from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.admin_schema import (SellerApproval, UserBlock, ReturnDecision)
from app.services.admin_service import (block_user, decide_seller, decide_return, refund_order)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User
from app.utils.rate_limiter import RateLimiter

admin_rate_limit = RateLimiter(limit=50, window_seconds=60, key_prefix="admin")
router = APIRouter(prefix="/admin", dependencies=[Depends(admin_rate_limit)] ,tags=["admin"])

@router.patch("/users/{user_id}")
async def block_unblock_user(user_id: int, data: UserBlock, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await block_user(db=db, user_id=user_id, blocked=data.blocked)

@router.post("/sellers/{seller_id}/decision")
async def seller_decision(seller_id: int, data: SellerApproval, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await decide_seller(db=db, seller_id=seller_id, approved=data.approved, commission_percent=data.commission_percent)

@router.post("/orders.{order_id}/return-decision")
async def return_decision(order_id: int, data: ReturnDecision, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await decide_return(db=db, order_id=order_id, approved=data.approved)

@router.post("/orders/{order_id}/refund")
async def refund(order_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    await refund_order(db, order_id)
    return {"status" : "refund initiated"}

