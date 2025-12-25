from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.models.seller_model import Seller, SellerKYCStatus
from app.models.order_model import Order, ReturnStatus
from app.services.payment_service import initiate_refund
from app.core.exceptions import(NotFoundException, ConflictException)


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
    return order


async def refund_order(db: AsyncSession, order_id: int):
    order = await db.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")
    if not order.is_returned:
        raise ConflictException("Order not returned")
    
    await initiate_refund(db, order_id)
    
