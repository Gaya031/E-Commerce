from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.seller_model import Seller
from app.core.exceptions import (ConflictException, NotFoundException, PermissionDeniedException)
from datetime import datetime

async def create_seller_profile(db: AsyncSession, user_id: int, store_name: str) -> Seller:
    existing = await db.execute(select(Seller).where(Seller.user_id == user_id))
    if existing.scalars().first():
        raise ConflictException("Seller profile already exists")
    
    seller = Seller(
        user_id=user_id,
        store_name=store_name,
        approved=False
    )
    
    db.add(seller)
    await db.commit()
    await db.refresh()
    return seller

async def upload_kyc(db: AsyncSession, seller_id: int, kyc_data: dict, user_id: int) -> Seller:
    result = await db.execute(select(Seller).where(Seller.id == user_id))
    seller = result.scalars().first()
    
    if not seller:
        raise NotFoundException("Seller not found")
    
    if seller.user_id != user_id:
        raise PermissionDeniedException("Not your seller profile")
    
    seller.kyc_docs = kyc_data
    await db.commit()
    return seller

async def approve_seller(db: AsyncSession, seller_id: int, commission_percent: int) -> Seller:
    result = await db.execute(select(Seller).where(Seller.id == seller_id))
    seller = result.scalars().first()
    
    if not seller:
        raise NotFoundException("seller not found")
    
    seller.approved = True
    seller.commission_percent = commission_percent
    await db.commit()
    return seller
