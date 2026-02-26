from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import case, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import require_roles
from app.db.postgres import get_db
from app.models.commission_model import Commission
from app.models.notification_model import NotificationType
from app.models.order_model import Order, OrderStatus
from app.models.order_item_model import OrderItem
from app.models.seller_model import Seller
from app.models.user_model import User
from app.schemas.seller_schema import SellerCreate, SellerKYCUpdate, SellerOut, SellerUpdate
from app.services.notification_service import create_notification
from app.services.order_service import get_order_items_map
from app.services.seller_service import (
    approve_seller,
    create_seller_profile,
    get_seller_by_user_id,
    update_seller_profile,
    upload_kyc,
    upload_kyc_for_user,
)
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_status_email

router = APIRouter(tags=["sellers"])


async def _get_seller_for_user(db: AsyncSession, user_id: int) -> Seller:
    seller = await get_seller_by_user_id(db, user_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
    return seller


@router.post("/", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
async def create_seller(
    data: SellerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    return await create_seller_profile(
        db=db,
        user_id=current_user.id,
        store_name=data.store_name,
        data=data.model_dump(exclude={"store_name"}, exclude_none=True),
    )


@router.put("/{seller_id}/kyc", response_model=SellerOut)
async def update_kyc(
    seller_id: int,
    data: SellerKYCUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    return await upload_kyc(
        db=db,
        seller_id=seller_id,
        kyc_data=data.model_dump(exclude_none=True),
        user_id=current_user.id,
    )


@router.post("/{seller_id}/approve", response_model=SellerOut)
async def approve(
    seller_id: int,
    commission_percent: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    return await approve_seller(
        db=db,
        seller_id=seller_id,
        commission_percent=commission_percent,
    )


@router.get("/me", response_model=SellerOut)
async def get_my_seller_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    return seller


@router.put("/me", response_model=SellerOut)
async def update_my_seller_profile(
    data: SellerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="No profile fields provided")
    return await update_seller_profile(db=db, user_id=current_user.id, data=payload)


@router.put("/me/kyc", response_model=SellerOut)
async def update_my_kyc(
    data: SellerKYCUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    return await upload_kyc_for_user(db=db, user_id=current_user.id, kyc_data=data.model_dump(exclude_none=True))


@router.get("/me/approval-status")
async def approval_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    return {"approved": seller.approved, "kyc_status": seller.kyc_status}


@router.get("/me/orders")
async def my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    result = await db.execute(select(Order).where(Order.seller_id == seller.id).order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    items_map = await get_order_items_map(db, [order.id for order in orders])
    data = []
    for o in orders:
        items = items_map.get(o.id, [])
        data.append(
            {
                "id": o.id,
                "status": o.status.value,
                "total_amount": float(o.total_amount),
                "items": [
                    {"product_id": i.product_id, "quantity": i.quantity, "price": float(i.price)} for i in items
                ],
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
        )
    return data


@router.get("/me/earnings-summary")
async def earnings_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    delivered_stats = await db.execute(
        select(
            func.count(Order.id).label("completed_orders"),
            func.coalesce(func.sum(Order.total_amount), 0).label("gross_revenue"),
        ).where(Order.seller_id == seller.id, Order.status == OrderStatus.delivered)
    )
    row = delivered_stats.one()
    return {
        "completed_orders": int(row.completed_orders or 0),
        "gross_revenue": int(row.gross_revenue or 0),
    }


@router.get("/me/commission-details")
async def commission_details(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    rows = await db.execute(
        select(Commission).where(Commission.seller_id == seller.id).order_by(Commission.created_at.desc())
    )
    commissions = rows.scalars().all()
    total_platform = sum(int(c.commission_amount) for c in commissions)
    total_earning = sum(int(c.seller_earning) for c in commissions)
    return {
        "current_commission_percent": seller.commission_percent,
        "total_platform_commission": total_platform,
        "total_seller_earnings": total_earning,
        "rows": commissions,
    }


@router.get("/me/dashboard-stats")
async def dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)

    orders_stats = await db.execute(
        select(
            func.count(Order.id).label("total_orders"),
            func.sum(case((Order.status == OrderStatus.delivered, 1), else_=0)).label("delivered_orders"),
            func.sum(case((Order.status.in_([OrderStatus.placed, OrderStatus.packed]), 1), else_=0)).label(
                "pending_orders"
            ),
            func.coalesce(
                func.sum(case((Order.status == OrderStatus.delivered, Order.total_amount), else_=0)),
                0,
            ).label("total_revenue"),
        ).where(Order.seller_id == seller.id)
    )
    row = orders_stats.one()

    product_stats = await db.execute(select(func.count()).select_from(OrderItem).join(Order, OrderItem.order_id == Order.id).where(Order.seller_id == seller.id))
    total_items_sold = int(product_stats.scalar() or 0)

    latest_orders = await db.execute(
        select(Order).where(Order.seller_id == seller.id).order_by(Order.created_at.desc()).limit(5)
    )
    latest = latest_orders.scalars().all()
    latest_items_map = await get_order_items_map(db, [o.id for o in latest])

    return {
        "total_orders": int(row.total_orders or 0),
        "delivered_orders": int(row.delivered_orders or 0),
        "pending_orders": int(row.pending_orders or 0),
        "total_revenue": int(row.total_revenue or 0),
        "total_items_sold": total_items_sold,
        "latest_orders": [
            {
                "id": o.id,
                "status": o.status.value,
                "total_amount": float(o.total_amount),
                "items_count": len(latest_items_map.get(o.id, [])),
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in latest
        ],
    }


@router.patch("/me/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    order = await db.get(Order, order_id)
    if not order or order.seller_id != seller.id:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status in (OrderStatus.cancelled, OrderStatus.delivered):
        raise HTTPException(status_code=400, detail="Finalized orders cannot be updated")

    allowed_statuses = {OrderStatus.packed, OrderStatus.shipped}
    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Seller can update only to packed/shipped")

    order.status = status
    await db.commit()
    await db.refresh(order)

    buyer = await db.get(User, order.buyer_id)
    if buyer:
        await create_notification(
            db=db,
            user_id=buyer.id,
            data={
                "title": f"Order #{order.id} updated",
                "message": f"Your order is now {order.status.value}.",
                "type": NotificationType.order,
                "link": f"/buyer/order/{order.id}/tracking",
            },
        )
        subject, body = order_status_email(buyer.name, order.id, order.status.value)
        send_email_background(buyer.email, subject, body)

    return {"id": order.id, "status": order.status.value}


@router.get("/me/subscription-status")
async def subscription_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("seller")),
):
    seller = await _get_seller_for_user(db, current_user.id)
    return {
        "subscription_plan_id": seller.subscription_plan_id,
        "subscription_expiry": seller.subscription_expiry.isoformat() if seller.subscription_expiry else None,
        "approved": seller.approved,
    }
