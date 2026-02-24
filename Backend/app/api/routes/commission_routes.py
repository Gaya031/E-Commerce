from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.commission_schema import CommissionOut
from app.services.commission_service import calculate_commission
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter(prefix="/commissions", tags = ["commissions"])

#Admin triggers commission calculation
@router.post("/calculate/{order_id}", response_model=CommissionOut, status_code=status.HTTP_201_CREATED)
async def calculate(order_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await calculate_commission(db=db, order_id=order_id)

