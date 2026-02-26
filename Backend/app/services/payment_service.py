import asyncio
import hashlib
import hmac
import json
from datetime import datetime, timezone

import razorpay
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, NotFoundException, PermissionDeniedException
from app.models.notification_model import NotificationType
from app.models.order_model import Order, OrderStatus, PaymentMethod
from app.models.payment_model import Payment, PaymentStatus
from app.models.user_model import User
from app.services.notification_service import create_notification
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_status_email


def _gateway_enabled() -> bool:
    return bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET)


def _new_razorpay_client() -> razorpay.Client:
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def _verify_checkout_signature(razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
    payload = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
    expected = hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, razorpay_signature)


async def _notify_payment_success(db: AsyncSession, order: Order):
    user = await db.get(User, order.buyer_id)
    if not user:
        return
    await create_notification(
        db=db,
        user_id=user.id,
        data={
            "title": f"Payment successful for order #{order.id}",
            "message": "Your payment was successful and order is being packed.",
            "type": NotificationType.payment,
            "link": f"/buyer/order/{order.id}/tracking",
        },
    )
    subject, body = order_status_email(user.name, order.id, order.status.value)
    send_email_background(user.email, subject, body)


async def initiate_payment(db: AsyncSession, order_id: int, user_id: int) -> dict:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    if order.buyer_id != user_id:
        raise PermissionDeniedException("You are not allowed to pay this order")
    if order.payment_method != PaymentMethod.prepaid:
        raise ConflictException("Order is not prepaid")
    if order.status == OrderStatus.cancelled:
        raise ConflictException("Cancelled order cannot be paid")

    payment_row = await db.execute(select(Payment).where(Payment.order_id == order.id))
    payment = payment_row.scalars().first()
    if not payment:
        payment = Payment(order_id=order.id, amount=order.total_amount)
        db.add(payment)
        await db.flush()

    if payment.status == PaymentStatus.completed:
        return {
            "payment_id": payment.id,
            "gateway": "completed",
            "amount": payment.amount,
            "amount_paise": payment.amount * 100,
            "status": payment.status.value,
        }

    if _gateway_enabled():
        if not payment.razorpay_order_id:
            payload = {
                "amount": int(payment.amount) * 100,
                "currency": "INR",
                "receipt": f"order_{order.id}_{int(datetime.now(tz=timezone.utc).timestamp())}",
            }
            client = _new_razorpay_client()
            razorpay_order = await asyncio.to_thread(client.order.create, payload)
            payment.razorpay_order_id = razorpay_order.get("id")
        payment.status = PaymentStatus.initiated
        await db.commit()
        await db.refresh(payment)
        return {
            "payment_id": payment.id,
            "gateway": "razorpay",
            "razorpay_order_id": payment.razorpay_order_id,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "amount": payment.amount,
            "amount_paise": payment.amount * 100,
            "currency": "INR",
            "status": payment.status.value,
        }

    payment.status = PaymentStatus.initiated
    await db.commit()
    await db.refresh(payment)
    return {
        "payment_id": payment.id,
        "gateway": "mock",
        "amount": payment.amount,
        "amount_paise": payment.amount * 100,
        "currency": "INR",
        "status": payment.status.value,
    }


async def confirm_payment(
    db: AsyncSession,
    user_id: int,
    payment_id: int,
    razorpay_order_id: str | None = None,
    razorpay_payment_id: str | None = None,
    razorpay_signature: str | None = None,
) -> dict:
    payment = await db.get(Payment, payment_id)
    if not payment:
        raise NotFoundException("Payment not found")

    order = await db.get(Order, payment.order_id)
    if not order:
        raise NotFoundException("Order not found")
    if order.buyer_id != user_id:
        raise PermissionDeniedException("You are not allowed to confirm this payment")
    if payment.status == PaymentStatus.completed:
        return {"payment_id": payment.id, "status": payment.status.value, "order_status": order.status.value}

    if payment.razorpay_order_id:
        if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
            raise ConflictException("Razorpay payment details are required")
        if payment.razorpay_order_id != razorpay_order_id:
            raise ConflictException("Razorpay order mismatch")
        if not _verify_checkout_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            raise ConflictException("Invalid Razorpay payment signature")
        payment.razorpay_payment_id = razorpay_payment_id

    payment.status = PaymentStatus.completed
    if order.status == OrderStatus.placed:
        order.status = OrderStatus.packed

    await db.commit()
    await _notify_payment_success(db, order)
    return {"payment_id": payment.id, "status": payment.status.value, "order_status": order.status.value}


async def verify_payment(db: AsyncSession, payload: dict, signature: str):
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    generated_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()

    if settings.RAZORPAY_WEBHOOK_SECRET and not hmac.compare_digest(generated_signature, signature):
        raise ConflictException("Invalid webhook signature")

    event = payload.get("event")
    if event != "payment.captured":
        return

    entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    webhook_payment_id = entity.get("id")
    webhook_order_id = entity.get("order_id")
    if not webhook_payment_id and not webhook_order_id:
        return

    result = await db.execute(
        select(Payment).where(
            or_(
                Payment.razorpay_payment_id == webhook_payment_id,
                Payment.razorpay_order_id == webhook_order_id,
            )
        )
    )
    payment = result.scalars().first()
    if not payment:
        raise NotFoundException("Payment not found")

    payment.razorpay_payment_id = webhook_payment_id or payment.razorpay_payment_id
    payment.status = PaymentStatus.completed

    order = await db.get(Order, payment.order_id)
    if order and order.status == OrderStatus.placed:
        order.status = OrderStatus.packed

    await db.commit()
    if order:
        await _notify_payment_success(db, order)


async def initiate_refund(db: AsyncSession, order_id: int):
    result = await db.execute(select(Payment).where(Payment.order_id == order_id))
    payment = result.scalars().first()

    if not payment:
        raise NotFoundException("Payment not found")

    if payment.status != PaymentStatus.completed:
        raise ConflictException("Payment not refundable")

    if payment.razorpay_payment_id and _gateway_enabled():
        client = _new_razorpay_client()
        refund_payload = {"payment_id": payment.razorpay_payment_id, "amount": int(payment.amount) * 100}
        refund = await asyncio.to_thread(client.payment.refund, payment.razorpay_payment_id, refund_payload)
        payment.razorpay_refund_id = refund.get("id")

    payment.status = PaymentStatus.refunded
    await db.commit()
