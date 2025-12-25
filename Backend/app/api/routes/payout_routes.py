from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.services.payout_service import(create_delivery_payout, create_seller_payout)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter(prefix="/payouts", tags=["payouts"])

@router.post("/seller/{seller_id}")
async def payout_seller(seller_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await create_seller_payout(db, seller_id)

@router.post("/delivery/{partner_id}")
async def payout_delivery_partner(partner_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await create_delivery_payout(db, partner_id)

