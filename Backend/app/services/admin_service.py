from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.models.seller_model import Seller, SellerKYCStatus
from app.models.order_model import Order, ReturnStatus
from app.models.notification_model import NotificationType
from app.services.payment_service import initiate_refund
from app.core.exceptions import(NotFoundException, ConflictException)
from app.core.logging import logger
from app.services.notification_service import create_notification
from app.services.search_service import upsert_store_document
from app.utils.simple_cache import cache_delete_prefix
from app.utils.email_handler import send_email_background
from app.utils.email_templates import order_status_email, refund_email, seller_approval_email


async def block_user(db: AsyncSession, user_id: int, blocked: bool) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException("User not found")
    
    user.is_blocked = blocked
    await db.commit()
    return user

async def decide_seller(db: AsyncSession, seller_id: int, approved: bool, commission_percent: int | None) -> Seller:
    seller = await db.get(Seller, seller_id)
    if not seller:
        raise NotFoundException("Seller not found")
    
    if approved:
        if commission_percent is None:
            raise ConflictException("Commission percent required")
        seller.approved = True
        seller.kyc_status = SellerKYCStatus.approved
        seller.commission_percent = commission_percent
    else:
        seller.approved = False
        seller.kyc_status = SellerKYCStatus.rejected
        
    await db.commit()
    await db.refresh(seller)
    user = await db.get(User, seller.user_id)
    if user:
        await create_notification(
            db=db,
            user_id=user.id,
            data={
                "title": "Seller verification update",
                "message": f"Your seller profile has been {'approved' if approved else 'rejected'}.",
                "type": NotificationType.system,
                "link": "/seller/approval-status",
            },
        )
        subject, body = seller_approval_email(user.name, approved)
        send_email_background(user.email, subject, body)
    try:
        await upsert_store_document(db, seller.id)
    except Exception as exc:
        logger.warning("Seller indexing failed for %s: %s", seller.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller

async def decide_return(db: AsyncSession, order_id: int, approved: bool) -> Order:
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    
    if order.return_status != ReturnStatus.requested:
        raise ConflictException("No pending return requested")
    if approved:
        order.return_status = ReturnStatus.approved
    else:
        order.return_status = ReturnStatus.rejected
        
    await db.commit()
    user = await db.get(User, order.buyer_id)
    if user:
        await create_notification(
            db=db,
            user_id=user.id,
            data={
                "title": f"Return {'approved' if approved else 'rejected'}",
                "message": f"Your return request for order #{order.id} has been {'approved' if approved else 'rejected'}.",
                "type": NotificationType.order,
                "link": f"/buyer/order/{order.id}",
            },
        )
        subject, body = order_status_email(user.name, order.id, f"return_{order.return_status.value}")
        send_email_background(user.email, subject, body)
    return order


async def refund_order(db: AsyncSession, order_id: int):
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    if not order.is_returned:
        raise ConflictException("Order not returned")
    
    await initiate_refund(db, order_id)
    user = await db.get(User, order.buyer_id)
    if user:
        await create_notification(
            db=db,
            user_id=user.id,
            data={
                "title": f"Refund initiated for order #{order.id}",
                "message": "Your refund is being processed.",
                "type": NotificationType.payment,
                "link": "/buyer/orders",
            },
        )
        subject, body = refund_email(user.name, order.id)
        send_email_background(user.email, subject, body)
    
