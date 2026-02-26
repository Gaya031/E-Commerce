from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import get_current_user
from app.db.postgres import get_db
from app.models.notification_model import NotificationType
from app.models.user_model import User
from app.schemas.order_schema import OrderCreate, OrderOut, ReturnRequest
from app.services.notification_service import create_notification
from app.services.order_service import (
    cancel_order,
    create_order,
    get_order_items_map,
    get_order_for_user,
    list_buyer_orders,
    request_return,
)
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_created_email, order_status_email
from app.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/orders", tags=["orders"])
place_order_rate_limit = RateLimiter(limit=10, window_seconds=60, key_prefix="place_order")


def _serialize_order(order, items):
    return {
        "id": order.id,
        "status": order.status.value,
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
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    orders = await list_buyer_orders(db, user.id)
    items_map = await get_order_items_map(db, [order.id for order in orders])
    data = []
    for order in orders:
        data.append(_serialize_order(order, items_map.get(order.id, [])))
    return data


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await get_order_for_user(db, order_id, user.id)
    items_map = await get_order_items_map(db, [order.id])
    return _serialize_order(order, items_map.get(order.id, []))


@router.post("/{order_id}/cancel")
async def cancel_order_route(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await cancel_order(db, order_id, user.id)
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
    return {"id": order.id, "status": order.status.value}


@router.post("/{order_id}/return")
async def return_order_route(
    order_id: int,
    data: ReturnRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = await request_return(db, order_id, user.id, data.reason, data.image)
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
