from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.models.notification_model import NotificationType
from app.models.order_model import Order, OrderStatus, PaymentMethod, ReturnStatus
from app.models.payment_model import Payment, PaymentStatus
from app.models.user_model import User
from app.models.wallet_model import WalletTransaction
from app.services.notification_service import create_notification
from app.services.payment_service import initiate_refund
from app.services.wallet_service import credit_wallet
from app.utils.email_handler import send_email_background
from app.utils.email_templates import refund_email


async def process_refund(db: AsyncSession, order_id: int) -> dict:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")

    is_return_refund = order.return_status in {ReturnStatus.approved, ReturnStatus.picked} or bool(order.is_returned)
    is_cancel_refund = order.status == OrderStatus.cancelled
    if not is_return_refund and not is_cancel_refund:
        raise ConflictException("Refund can only be processed for cancelled or returned orders")

    refund_status = "processed"
    refund_mode = "none"
    should_notify = True

    if order.payment_method == PaymentMethod.prepaid:
        payment_result = await db.execute(select(Payment).where(Payment.order_id == order.id))
        payment = payment_result.scalars().first()
        if not payment:
            raise ConflictException("No payment found for prepaid order")
        if payment.status == PaymentStatus.refunded:
            refund_status = "already_refunded"
            refund_mode = "gateway"
            should_notify = False
        elif payment.status != PaymentStatus.completed:
            raise ConflictException("Payment is not refundable in current state")
        else:
            await initiate_refund(db, order.id)
            refund_mode = "gateway"
    else:
        if not is_return_refund:
            raise ConflictException("COD refund is only allowed after return approval")
        txn_result = await db.execute(
            select(WalletTransaction).where(
                WalletTransaction.user_id == order.buyer_id,
                WalletTransaction.type == "cod_refund",
                WalletTransaction.reference_id == str(order.id),
            )
        )
        existing_txn = txn_result.scalars().first()
        if existing_txn:
            refund_status = "already_refunded"
            refund_mode = "wallet"
            should_notify = False
        else:
            await credit_wallet(
                db=db,
                user_id=order.buyer_id,
                amount=order.total_amount,
                txn_type="cod_refund",
                reference_id=str(order.id),
            )
            refund_mode = "wallet"

    if order.status != OrderStatus.cancelled:
        order.status = OrderStatus.cancelled
    if is_return_refund:
        order.is_returned = True
    await db.commit()

    if should_notify:
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

    return {
        "order_id": order.id,
        "status": order.status.value,
        "refund_status": refund_status,
        "refund_mode": refund_mode,
    }
    
