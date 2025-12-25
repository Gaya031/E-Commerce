from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.wallet_schema import WalletOut
from app.models.wallet_model import WalletTransaction
from app.api.deps.auth_deps import get_current_user
from app.models.user_model import User
from sqlalchemy import select

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/", response_model=WalletOut)
async def get_wallet(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    txns = await db.execute(
        select(WalletTransaction)
        .where(WalletTransaction.user_id == user.id)
        .order_by(WalletTransaction.created_at.desc())
    )
    return {
        "balance": user.wallet_balance,
        "transactions": txns.scalars().all()
    }
    
