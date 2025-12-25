from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order_model import Order, OrderStatus, ReturnStatus, PaymentMethod
from app.models.payment_model import Payment, PaymentStatus
from app.services.wallet_service import credit_wallet
from app.services.payment_service import initiate_refund
from app.core.exceptions import ConflictException

async def process_refund(db: AsyncSession, order_id: int):
    order = await db.get(Order, order_id)
    if not order:
        raise ConflictException("order not found")
    if order.return_status != ReturnStatus.picked:
        raise ConflictException("return not completed")
    
    # prevent double refund
    if order.status == OrderStatus.cancelled:
        raise ConflictException("Refund already processed")
    if order.payment_method == PaymentMethod.prepaid:
        await initiate_refund(db, order_id)
        
    else:
        await credit_wallet(
            db=db, 
            user_id=order.buyer_id,
            amount=order.total_amount,
            txn_type="cod_refund",
            reference_id=str(order.id)
        )
        
    order.status = OrderStatus.cancelled
    await db.commit()
    