from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import get_current_user
from app.db.postgres import get_db
from app.models.notification_model import NotificationType
from app.models.user_model import User
from app.schemas.order_schema import OrderCreate, OrderOut, ReturnRequest
from app.services.notification_service import create_notification
from app.services.order_service import (
    can_cancel_order,
    cancel_order,
    create_order,
    get_buyer_order_summary,
    get_order_items_map,
    get_order_for_user,
    list_buyer_orders,
    request_return,
)
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_created_email, order_status_email
from app.utils.rate_limiter import RateLimiter
from app.utils.simple_cache import cache_delete_prefix, cache_get, cache_set

router = APIRouter(prefix="/orders", tags=["orders"])
place_order_rate_limit = RateLimiter(limit=10, window_seconds=60, key_prefix="place_order")


def _serialize_order(order, items):
    return {
        "id": order.id,
        "status": order.status.value,
        "can_cancel": can_cancel_order(order.status),
        "total_amount": float(order.total_amount),
        "payment_method": order.payment_method.value,
        "address": order.address,
        "return_status": order.return_status.value if order.return_status else None,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": [
            {
                "product_id": i.product_id,
                "quantity": i.quantity,
                "price": float(i.price),
            }
            for i in items
        ],
    }


@router.post("/", response_model=OrderOut)
async def place_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _rate_limit: None = Depends(place_order_rate_limit),
):
    order = await create_order(db, user.id, payload)
    await cache_delete_prefix(f"orders:buyer:{user.id}:")
    await create_notification(
        db=db,
        user_id=user.id,
        data={
            "title": f"Order #{order.id} placed",
            "message": "Your order has been placed successfully.",
            "type": NotificationType.order,
            "link": f"/buyer/order/{order.id}/tracking",
        },
    )
    subject, body = order_created_email(user.name, order.id, int(order.total_amount))
    send_email_background(user.email, subject, body)
    return {
        "order_id": order.id,
        "status": order.status.value,
        "total_amount": float(order.total_amount),
    }


@router.get("/")
async def list_orders(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    include_items: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cache_key = f"orders:buyer:{user.id}:list:p{page}:s{size}:items{int(include_items)}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    offset = (page - 1) * size
    orders = await list_buyer_orders(db, user.id, offset=offset, limit=size)
    items_map = {}
    if include_items:
        items_map = await get_order_items_map(db, [order.id for order in orders])

    payload = [_serialize_order(order, items_map.get(order.id, [])) for order in orders]
    await cache_set(cache_key, payload, ttl_seconds=20)
    return payload


@router.get("/summary")
async def order_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cache_key = f"orders:buyer:{user.id}:summary"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    payload = await get_buyer_order_summary(db, user.id)
    await cache_set(cache_key, payload, ttl_seconds=20)
    return payload


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cache_key = f"orders:buyer:{user.id}:detail:{order_id}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    order = await get_order_for_user(db, order_id, user.id)
    items_map = await get_order_items_map(db, [order.id])
    payload = _serialize_order(order, items_map.get(order.id, []))
    await cache_set(cache_key, payload, ttl_seconds=20)
    return payload


@router.post("/{order_id}/cancel")
async def cancel_order_route(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order, refund_status = await cancel_order(db, order_id, user.id)
    await cache_delete_prefix(f"orders:buyer:{user.id}:")
    await create_notification(
        db=db,
        user_id=user.id,
        data={
            "title": f"Order #{order.id} cancelled",
            "message": "Your order has been cancelled.",
            "type": NotificationType.order,
            "link": f"/buyer/orders",
        },
    )
    subject, body = order_status_email(user.name, order.id, order.status.value)
    send_email_background(user.email, subject, body)
    return {"id": order.id, "status": order.status.value, "refund_status": refund_status}


@router.post("/{order_id}/return")
async def return_order_route(
    order_id: int,
    data: ReturnRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await request_return(db, order_id, user.id, data.reason, data.image)
    await cache_delete_prefix(f"orders:buyer:{user.id}:")
    await create_notification(
        db=db,
        user_id=user.id,
        data={
            "title": f"Return requested for order #{order.id}",
            "message": "Your return request was submitted successfully.",
            "type": NotificationType.order,
            "link": f"/buyer/order/{order.id}",
        },
    )
    return {"id": order.id, "return_status": order.return_status.value}
