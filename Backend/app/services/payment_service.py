import hmac
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.payment_model import Payment, PaymentStatus
from app.models.order_model import Order, OrderStatus, PaymentMethod
from app.core.exceptions import NotFoundException, ConflictException
from app.core.config import settings

async def initiate_payment(db: AsyncSession, order_id: int) -> dict:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    
    if not order:
        raise NotFoundException("Order not found")
    
    if order.payment_method != PaymentMethod.prepaid:
        raise ConflictException("Order is not prepaid")
    
    payment = Payment(
        order_id = order.id,
        amount = order.total_amount
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    return {
        "payment_id": payment.id,
        "amount": payment.amount
    }
    
async def verify_payment(db: AsyncSession, payload: dict, signature: str):
    generated_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    
    if generated_signature != signature:
        raise ConflictException("Invalid webhook signature")
    
    event = payload.get("event")
    
    if event == "payment.captured":
        payment_id = payload["payload"]["payment"]["entity"]["id"]
        
        result = await db.execute(select(Payment).where(Payment.razorpay_payment_id == payment_id))
        payment = result.scalars().first()
        
        if not payment:
            raise NotFoundException("Payment not found")
        
        payment.status = PaymentStatus.completed
        
        order = await db.get(Order, payment.order_id)
        order.status = OrderStatus.packed
        
        await db.commit()
        

async def initiate_refund(db: AsyncSession, order_id: int):
    result = await db.execute(select(Payment).where(Payment.order_id == order_id))
    payment = result.scalars().first()
    
    if not payment:
        raise NotFoundException("Payment not found")
    
    if payment.status != PaymentStatus.completed:
        raise ConflictException("Payment not refundable")
    
    payment.status = PaymentStatus.refunded
    await db.commit()
    
    