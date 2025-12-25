from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.delivery_schema import (DeliveryAssign, DeliveryStatusUpdate)
from app.services.delivery_service import (assign_delivery_partner, update_delivery_status)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter(prefix="/delivery", tags=["delivery"])

@router.post("/assign", status_code=status.HTTP_201_CREATED)
async def assign(data: DeliveryAssign, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await assign_delivery_partner(
        db=db,
        order_id=data.order_id,
        partner_id=data.partner_id,
        distance_km=data.distance_km
    )
    
@router.patch("/{delivery_id}/status")
async def update_status(delivery_id: int, data: DeliveryStatusUpdate, db: AsyncSession = Depends(get_db), partner: User = Depends(require_roles("delivery"))):
    return await update_delivery_status(db=db, delivery_id=delivery_id, partner_id=partner.id, status=data.status)

