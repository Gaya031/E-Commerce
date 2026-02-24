from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product_model import Product
from app.models.seller_model import Seller
from app.core.exceptions import (PermissionDeniedException, NotFoundException, ConflictException)


async def get_approved_seller(db: AsyncSession, user_id: int) -> Seller:
    result = await db.execute(select(Seller).where(Seller.user_id == user_id))
    seller = result.scalars().first()
    
    if not seller:
        raise NotFoundException("seller profile not found")
    
    if not seller.approved:
        raise PermissionDeniedException("seller not approved")
    
    return seller


async def create_product(db: AsyncSession, user_id: int, data: dict) -> Product:
    seller = await get_approved_seller(db, user_id)
    product = Product(
        seller_id = seller.id,
        **data,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(db: AsyncSession, product_id: int, user_id: int, data: dict) -> Product:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    
    if not product:
        raise NotFoundException("product not found")
    
    seller = await get_approved_seller(db, user_id)
    
    if product.seller_id != seller.id:
        raise PermissionDeniedException("Not your product")
    
    for key, value in data.items():
        setattr(product, key, value)
        
    await db.commit()
    return product


async def update_stock(db: AsyncSession, product_id: int, user_id: int, new_stock: int) -> Product:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    
    if not product:
        raise NotFoundException("Product not found")
    
    seller = await get_approved_seller(db, user_id)
    
    if product.seller_id != seller.id:
        raise PermissionDeniedException("Not your product")
    
    product.stock = new_stock
    await db.commit()
    return product


async def reduce_stock(db: AsyncSession, product_id: int, quantity: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    
    if not product:
        raise NotFoundException("Product not found")
    
    if product.stock < quantity:
        raise ConflictException("Insufficient stock")
    
    product.stock -= quantity
    await db.commit()

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    product = result.scalars().all()
    
    return product