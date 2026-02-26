from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.delivery_model import Delivery, DeliveryStatus
from app.models.order_model import Order, OrderStatus
from app.models.notification_model import NotificationType
from app.models.seller_model import Seller
from app.models.user_model import User
from app.core.exceptions import NotFoundException, ConflictException, PermissionDeniedException
from app.services.notification_service import create_notification
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_status_email

async def assign_delivery_partner(db: AsyncSession, order_id: int, partner_id: int, distance_km: int) -> Delivery:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    
    if order.status != OrderStatus.packed:
        raise ConflictException("Order not ready for delivery")
    
    result = await db.execute(select(Delivery).where(Delivery.order_id == order_id))
    if result.scalars().first():
        raise ConflictException("Delivery already assigned")
    
    delivery_fee = distance_km * 10  #example
    partner_earning = int(delivery_fee * 0.8)
    delivery = Delivery(
        order_id = order_id,
        partner_id = partner_id,
        distance_km = distance_km,
        delivery_fee = delivery_fee,
        partner_earning = partner_earning
    )
    order.delivery_partner_id = partner_id
    order.status = OrderStatus.shipped
    
    db.add(delivery)
    await db.commit()
    await db.refresh(delivery)
    return delivery

async def update_delivery_status(db: AsyncSession, delivery_id: int, partner_id: int, status: DeliveryStatus) -> Delivery:
    delivery = await db.get(Delivery, delivery_id)
    if not delivery:
        raise NotFoundException("Delivery not found")
    
    if delivery.partner_id != partner_id:
        raise ConflictException("Not your delivery")
    
    order = await db.get(Order, delivery.order_id)
    if status == DeliveryStatus.delivered and order:
        order.status = OrderStatus.delivered
        
    delivery.status = status
    await db.commit()
    await db.refresh(delivery)
    if order:
        user = await db.get(User, order.buyer_id)
        if user:
            await create_notification(
                db=db,
                user_id=user.id,
                data={
                    "title": f"Delivery update for order #{order.id}",
                    "message": f"Order status is now {order.status.value if status == DeliveryStatus.delivered else status.value}.",
                    "type": NotificationType.delivery,
                    "link": f"/buyer/order/{order.id}/tracking",
                },
            )
            subject, body = order_status_email(
                user.name,
                order.id,
                order.status.value if status == DeliveryStatus.delivered else status.value,
            )
            send_email_background(user.email, subject, body)
    return delivery


async def get_partner_deliveries(
    db: AsyncSession, partner_id: int, status: DeliveryStatus | None = None
) -> list[Delivery]:
    query = select(Delivery).where(Delivery.partner_id == partner_id)
    if status:
        query = query.where(Delivery.status == status)
    result = await db.execute(query.order_by(Delivery.created_at.desc()))
    return result.scalars().all()


async def get_partner_earnings_summary(db: AsyncSession, partner_id: int) -> dict:
    deliveries_result = await db.execute(
        select(func.count(Delivery.id)).where(
            Delivery.partner_id == partner_id, Delivery.status == DeliveryStatus.delivered
        )
    )
    earnings_result = await db.execute(
        select(func.coalesce(func.sum(Delivery.partner_earning), 0)).where(
            Delivery.partner_id == partner_id, Delivery.status == DeliveryStatus.delivered
        )
    )
    return {
        "completed_deliveries": deliveries_result.scalar() or 0,
        "total_earnings": int(earnings_result.scalar() or 0),
    }


def _coerce_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


async def get_delivery_route_context(db: AsyncSession, delivery_id: int, partner_id: int) -> dict:
    delivery = await db.get(Delivery, delivery_id)
    if not delivery:
        raise NotFoundException("Delivery not found")
    if delivery.partner_id != partner_id:
        raise PermissionDeniedException("Not your delivery")

    order = await db.get(Order, delivery.order_id)
    if not order:
        raise NotFoundException("Order not found")

    seller = await db.get(Seller, order.seller_id)

    address = order.address or {}
    coordinates = address.get("coordinates") if isinstance(address, dict) else None

    pickup_lat = _coerce_float(getattr(seller, "latitude", None))
    pickup_lng = _coerce_float(getattr(seller, "longitude", None))

    drop_lat = None
    drop_lng = None
    if isinstance(coordinates, dict):
        drop_lat = _coerce_float(coordinates.get("lat") or coordinates.get("latitude"))
        drop_lng = _coerce_float(coordinates.get("lng") or coordinates.get("longitude"))

    return {
        "delivery_id": delivery.id,
        "order_id": delivery.order_id,
        "status": delivery.status.value,
        "pickup": {
            "name": getattr(seller, "store_name", None) or "Pickup Store",
            "address": getattr(seller, "address", None),
            "lat": pickup_lat,
            "lng": pickup_lng,
        },
        "drop": {
            "name": address.get("name") if isinstance(address, dict) else "Customer",
            "address": address.get("house_no") if isinstance(address, dict) else None,
            "city": address.get("city") if isinstance(address, dict) else None,
            "state": address.get("state") if isinstance(address, dict) else None,
            "pincode": address.get("pincode") if isinstance(address, dict) else None,
            "lat": drop_lat,
            "lng": drop_lng,
        },
    }

