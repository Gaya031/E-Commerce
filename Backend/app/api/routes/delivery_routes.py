from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.delivery_schema import (DeliveryAssign, DeliveryStatusUpdate)
from app.services.delivery_service import (
    assign_delivery_partner,
    claim_delivery_for_partner,
    update_delivery_status,
    get_partner_deliveries,
    get_partner_earnings_summary,
    get_delivery_route_context,
    list_open_orders_for_delivery,
    generate_delivery_route,
    get_order_tracking,
    upsert_delivery_tracking,
)
from app.api.deps.auth_deps import get_current_user, require_roles
from app.models.user_model import User, UserRole
from app.models.delivery_model import DeliveryStatus
from app.models.order_model import Order
from app.models.seller_model import Seller

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


def _with_route_context(delivery_payload: dict, context: dict | None):
    if not context:
        return delivery_payload
    payload = dict(delivery_payload)
    payload["pickup"] = context.get("pickup")
    payload["drop"] = context.get("drop")
    return payload

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
    rows = await get_partner_deliveries(db=db, partner_id=partner.id)
    rows = [row for row in rows if row.status != DeliveryStatus.delivered]
    payload = []
    for row in rows:
        base = _delivery_to_dict(row)
        try:
            context = await get_delivery_route_context(db=db, delivery_id=row.id, partner_id=partner.id)
        except Exception:
            context = None
        payload.append(_with_route_context(base, context))
    open_orders = await list_open_orders_for_delivery(db=db, partner_id=partner.id)
    return payload + open_orders


@router.post("/claim/{order_id}")
async def claim_delivery(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    row = await claim_delivery_for_partner(db=db, order_id=order_id, partner_id=partner.id)
    base = _delivery_to_dict(row)
    try:
        context = await get_delivery_route_context(db=db, delivery_id=row.id, partner_id=partner.id)
    except Exception:
        context = None
    return _with_route_context(base, context)


@router.get("/assigned")
async def assigned_deliveries(
    include_delivered: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    rows = await get_partner_deliveries(db=db, partner_id=partner.id)
    if not include_delivered:
        rows = [row for row in rows if row.status != DeliveryStatus.delivered]
    payload = []
    for row in rows:
        base = _delivery_to_dict(row)
        try:
            context = await get_delivery_route_context(db=db, delivery_id=row.id, partner_id=partner.id)
        except Exception:
            context = None
        payload.append(_with_route_context(base, context))
    return payload


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


@router.get("/map/route")
async def route_map(
    from_lat: float = Query(...),
    from_lng: float = Query(...),
    to_lat: float = Query(...),
    to_lng: float = Query(...),
    _: User = Depends(require_roles("delivery", "admin")),
):
    return await generate_delivery_route(from_lat=from_lat, from_lng=from_lng, to_lat=to_lat, to_lng=to_lng)


@router.post("/tracking/location")
async def tracking_location(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    partner: User = Depends(require_roles("delivery")),
):
    delivery_id = payload.get("delivery_id")
    lat = payload.get("lat")
    lng = payload.get("lng")
    if delivery_id is None or lat is None or lng is None:
        raise HTTPException(status_code=400, detail="delivery_id, lat and lng are required")
    try:
        tracking = await upsert_delivery_tracking(
            db=db,
            delivery_id=int(delivery_id),
            partner_id=partner.id,
            order_id=int(payload["order_id"]) if payload.get("order_id") is not None else None,
            lat=float(lat),
            lng=float(lng),
            heading=float(payload["heading"]) if payload.get("heading") is not None else None,
            speed=float(payload["speed"]) if payload.get("speed") is not None else None,
            status=str(payload.get("status")) if payload.get("status") is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid numeric payload values") from exc
    return {"ok": True, "tracking": tracking}


@router.get("/tracking/order/{order_id}")
async def tracking_by_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role == UserRole.buyer and order.buyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this tracking")

    if current_user.role == UserRole.delivery:
        partner_delivery = await db.execute(
            select(Order.id).where(Order.id == order_id, Order.delivery_partner_id == current_user.id)
        )
        if partner_delivery.scalar() is None:
            raise HTTPException(status_code=403, detail="Not allowed to view this tracking")

    if current_user.role == UserRole.seller:
        seller_id_result = await db.execute(select(Seller.id).where(Seller.user_id == current_user.id))
        seller_id = seller_id_result.scalar()
        if not seller_id or seller_id != order.seller_id:
            raise HTTPException(status_code=403, detail="Not allowed to view this tracking")

    tracking = await get_order_tracking(db=db, order_id=order_id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Tracking not found")
    return tracking

