from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.delivery_schema import (DeliveryAssign, DeliveryStatusUpdate)
from app.services.delivery_service import (
    assign_delivery_partner,
    update_delivery_status,
    get_partner_deliveries,
    get_partner_earnings_summary,
    get_delivery_route_context,
)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User
from app.models.delivery_model import DeliveryStatus

router = APIRouter(prefix="/delivery", tags=["delivery"])


def _delivery_to_dict(row):
    return {
        "id": row.id,
        "order_id": row.order_id,
        "partner_id": row.partner_id,
        "status": row.status.value,
        "distance_km": row.distance_km,
        "delivery_fee": row.delivery_fee,
        "partner_earning": row.partner_earning,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }

@router.post("/assign", status_code=status.HTTP_201_CREATED)
async def assign(data: DeliveryAssign, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    delivery = await assign_delivery_partner(
        db=db,
        order_id=data.order_id,
        partner_id=data.partner_id,
        distance_km=data.distance_km
    )
    return _delivery_to_dict(delivery)
    
@router.patch("/{delivery_id}/status")
async def update_status(delivery_id: int, data: DeliveryStatusUpdate, db: AsyncSession = Depends(get_db), partner: User = Depends(require_roles("delivery"))):
    delivery = await update_delivery_status(db=db, delivery_id=delivery_id, partner_id=partner.id, status=data.status)
    return _delivery_to_dict(delivery)


@router.get("/available")
async def available_deliveries(
    db: AsyncSession = Depends(get_db), partner: User = Depends(require_roles("delivery"))
):
    # In current workflow, deliveries are pre-assigned by admin.
    rows = await get_partner_deliveries(db=db, partner_id=partner.id, status=DeliveryStatus.assigned)
    return [_delivery_to_dict(r) for r in rows]


@router.get("/assigned")
async def assigned_deliveries(
    db: AsyncSession = Depends(get_db), partner: User = Depends(require_roles("delivery"))
):
    rows = await get_partner_deliveries(db=db, partner_id=partner.id)
    return [_delivery_to_dict(r) for r in rows]


@router.post("/{delivery_id}/pickup-confirmation")
async def pickup_confirmation(
    delivery_id: int,
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    row = await update_delivery_status(
        db=db, delivery_id=delivery_id, partner_id=partner.id, status=DeliveryStatus.picked
    )
    return _delivery_to_dict(row)


@router.post("/{delivery_id}/delivery-confirmation")
async def delivery_confirmation(
    delivery_id: int,
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    row = await update_delivery_status(
        db=db, delivery_id=delivery_id, partner_id=partner.id, status=DeliveryStatus.delivered
    )
    return _delivery_to_dict(row)


@router.get("/earnings-summary")
async def earnings_summary(
    db: AsyncSession = Depends(get_db), partner: User = Depends(require_roles("delivery"))
):
    return await get_partner_earnings_summary(db=db, partner_id=partner.id)


@router.get("/{delivery_id}/route-context")
async def route_context(
    delivery_id: int,
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    return await get_delivery_route_context(db=db, delivery_id=delivery_id, partner_id=partner.id)

