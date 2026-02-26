from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order_model import Order, OrderStatus, ReturnStatus, PaymentMethod
from app.models.payment_model import Payment, PaymentStatus
from app.models.notification_model import NotificationType
from app.models.user_model import User
from app.services.wallet_service import credit_wallet
from app.services.payment_service import initiate_refund
from app.services.notification_service import create_notification
from app.core.exceptions import ConflictException
from app.utils.email_handler import send_email_background
from app.utils.email_templates import refund_email

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
    user = await db.get(User, order.buyer_id)
    if user:
        await create_notification(
            db=db,
            user_id=user.id,
            data={
                "title": f"Refund completed for order #{order.id}",
                "message": "Your refund has been completed.",
                "type": NotificationType.payment,
                "link": "/buyer/wallet",
            },
        )
        subject, body = refund_email(user.name, order.id)
        send_email_background(user.email, subject, body)
    
