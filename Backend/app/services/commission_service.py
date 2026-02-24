from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.commission_model import Commission
from app.models.order_model import Order, OrderStatus, PaymentMethod
from app.models.payment_model import Payment, PaymentStatus
from app.models.seller_model import Seller
from app.core.exceptions import (ConflictException, NotFoundException)

async def calculate_commission(db: AsyncSession, order_id: int) -> Commission:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    
    existing = await db.execute(select(Commission).where(Commission.order_id == order_id))
    if existing.scalars().first():
        raise ConflictException("Commission already calculated")
    
    #validate payment condition
    if order.payment_method == PaymentMethod.prepaid:
        payment = await db.execute(select(Payment).where(Payment.order_id == order_id))
        payment = payment.scalars().first()
        
        if not payment or payment.status != PaymentStatus.completed:
            raise ConflictException("Payment not completed")
        
    if order.status != OrderStatus.delivered:
        raise ConflictException("Order not delivered")
    
    seller = await db.execute(select(Seller).where(Seller.id == order.seller_id))
    seller = seller.scalars().first()
    
    if not seller:
        raise NotFoundException("Seller not found")
    commission_percent = seller.commission_percent
    commission_amount = (order.total_amount * commission_percent) // 100
    seller_earning = order.total_amount - commission_amount
    platform_earning = commission_amount
    
    commission = Commission(
        order_id = order.id,
        seller_id = seller.id,
        commission_percent = commission_percent,
        commission_amount = commission_amount,
        seller_earning = seller_earning,
        platform_earning = platform_earning
    )
    
    db.add(commission)
    await db.commit()
    await db.refresh(commission)
    return commission

