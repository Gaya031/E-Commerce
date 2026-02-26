from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import require_roles
from app.db.postgres import get_db
from app.models.commission_model import Commission
from app.models.order_model import Order, OrderStatus, ReturnStatus
from app.models.seller_model import Seller
from app.models.user_model import User
from app.schemas.admin_schema import ReturnDecision, SellerApproval, UserBlock
from app.services.order_service import get_order_items_map
from app.services.admin_service import block_user, decide_return, decide_seller, refund_order
from app.utils.rate_limiter import RateLimiter

admin_rate_limit = RateLimiter(limit=50, window_seconds=60, key_prefix="admin")
router = APIRouter(prefix="/admin", dependencies=[Depends(admin_rate_limit)], tags=["admin"])


@router.patch("/users/{user_id}")
async def block_unblock_user(
    user_id: int,
    data: UserBlock,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    return await block_user(db=db, user_id=user_id, blocked=data.blocked)


@router.post("/sellers/{seller_id}/decision")
async def seller_decision(
    seller_id: int,
    data: SellerApproval,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    return await decide_seller(
        db=db, seller_id=seller_id, approved=data.approved, commission_percent=data.commission_percent
    )


@router.post("/orders/{order_id}/return-decision")
async def return_decision(
    order_id: int,
    data: ReturnDecision,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    return await decide_return(db=db, order_id=order_id, approved=data.approved)


@router.post("/orders/{order_id}/refund")
async def refund(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    await refund_order(db, order_id)
    return {"status": "refund initiated"}


@router.get("/sellers")
async def list_sellers(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(select(Seller).order_by(Seller.created_at.desc()))
    sellers = result.scalars().all()
    user_ids = [s.user_id for s in sellers]
    user_map = {}
    if user_ids:
        user_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        user_map = {user.id: user for user in user_result.scalars().all()}
    data = []
    for seller in sellers:
        user = user_map.get(seller.user_id)
        data.append(
            {
                "id": seller.id,
                "store_name": seller.store_name,
                "commission_percent": seller.commission_percent,
                "is_approved": seller.approved,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_blocked": user.is_blocked,
                }
                if user
                else None,
            }
        )
    return data


@router.get("/orders")
async def list_orders(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    items_map = await get_order_items_map(db, [order.id for order in orders])
    data = []
    for order in orders:
        items = items_map.get(order.id, [])
        data.append(
            {
                "id": order.id,
                "status": order.status.value,
                "total_amount": float(order.total_amount),
                "items": [
                    {
                        "product_id": i.product_id,
                        "quantity": i.quantity,
                        "price": float(i.price),
                    }
                    for i in items
                ],
                "created_at": order.created_at.isoformat() if order.created_at else None,
            }
        )
    return data


@router.get("/users")
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "phone": u.phone,
            "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            "wallet_balance": u.wallet_balance,
            "is_blocked": u.is_blocked,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]


@router.get("/returns")
async def pending_returns(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(
        select(Order).where(Order.return_status == ReturnStatus.requested).order_by(Order.created_at.desc())
    )
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "status": r.status.value,
            "return_status": r.return_status.value,
            "total_amount": float(r.total_amount),
        }
        for r in rows
    ]


@router.get("/refunds")
async def refund_queue(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(
        select(Order).where(Order.return_status.in_([ReturnStatus.approved, ReturnStatus.picked]))
    )
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "status": r.status.value,
            "return_status": r.return_status.value,
            "total_amount": float(r.total_amount),
        }
        for r in rows
    ]


@router.patch("/commission/config")
async def update_commission_config(
    seller_id: int,
    commission_percent: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    seller = await db.get(Seller, seller_id)
    if not seller:
        return {"updated": False, "reason": "seller not found"}
    seller.commission_percent = commission_percent
    await db.commit()
    return {"updated": True, "seller_id": seller_id, "commission_percent": commission_percent}


@router.get("/analytics/revenue")
async def revenue_analytics(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    total_orders = await db.execute(select(func.count(Order.id)))
    delivered_orders = await db.execute(
        select(func.count(Order.id)).where(Order.status == OrderStatus.delivered)
    )
    gross_revenue = await db.execute(select(func.coalesce(func.sum(Order.total_amount), 0)))
    platform_commission = await db.execute(select(func.coalesce(func.sum(Commission.commission_amount), 0)))
    return {
        "total_orders": int(total_orders.scalar() or 0),
        "delivered_orders": int(delivered_orders.scalar() or 0),
        "gross_revenue": int(gross_revenue.scalar() or 0),
        "platform_commission": int(platform_commission.scalar() or 0),
    }


@router.get("/reports/export")
async def export_report(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
):
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    lines = ["id,status,total_amount,created_at"]
    for o in orders:
        lines.append(f"{o.id},{o.status.value},{o.total_amount},{o.created_at.isoformat() if o.created_at else ''}")
    csv_data = "\n".join(lines)
    return Response(content=csv_data, media_type="text/csv")
