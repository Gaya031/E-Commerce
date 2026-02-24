from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.delivery_model import Delivery, DeliveryStatus
from app.models.order_model import Order, OrderStatus
from app.models.user_model import UserRole
from app.core.exceptions import (NotFoundException, ConflictException, PermissionDeniedException)

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
    
    if status == DeliveryStatus.delivered:
        order = await db.get(Order, delivery.order_id)
        order.status = OrderStatus.delivered
        
    delivery.status = status
    await db.commit()
    return delivery

