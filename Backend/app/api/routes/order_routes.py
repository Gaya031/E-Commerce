from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.order_schema import (OrderCreate, OrderStatusUpdate, ReturnRequest)
from app.services.order_service import (create_order, update_order_status, request_return)
from app.api.deps.auth_deps import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def place_order(data: OrderCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_order(
        db=db,
        buyer_id=user.id,
        data=data.model_dump()
    )


@router.patch("/{order_id}/status")
async def update_status(order_id: int, data: OrderStatusUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await update_order_status(
        db=db,
        order_id=order_id,
        user_id=user.id,
        new_status=data.status
    )

@router.post("/{order_id}/return")
async def return_order(order_id: int, data: ReturnRequest, db:AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await request_return(
        db = db,
        order_id=order_id,
        buyer_id=user.id,
        reason=data.reason,
        image=data.image
    )
    
