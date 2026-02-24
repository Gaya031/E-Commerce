from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.order_schema import OrderCreate, OrderOut
from app.services.order_service import create_order
from app.api.deps.auth_deps import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut)
async def place_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        order = await create_order(db, user.id, payload)
        return {
            "order_id": order.id,
            "status": order.status.value,
            "total_amount": float(order.total_amount),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))