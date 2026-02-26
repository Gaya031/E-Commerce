from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product_model import Product
from app.models.seller_model import Seller
from app.core.exceptions import (PermissionDeniedException, NotFoundException, ConflictException)
from app.core.logging import logger
from app.services.search_service import upsert_product_document
from app.utils.simple_cache import cache_delete_prefix


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
    try:
        await upsert_product_document(db, product.id)
    except Exception as exc:
        logger.warning("Product indexing failed for %s: %s", product.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
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
    await db.refresh(product)
    try:
        await upsert_product_document(db, product.id)
    except Exception as exc:
        logger.warning("Product indexing failed for %s: %s", product.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
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
    await db.refresh(product)
    try:
        await upsert_product_document(db, product.id)
    except Exception as exc:
        logger.warning("Product indexing failed for %s: %s", product.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
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
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")


async def delete_product(db: AsyncSession, product_id: int, user_id: int) -> bool:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise NotFoundException("Product not found")

    seller = await get_approved_seller(db, user_id)
    if product.seller_id != seller.id:
        raise PermissionDeniedException("Not your product")

    await db.delete(product)
    await db.commit()
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return True

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 50, only_active: bool = True):
    query = select(Product).offset(skip).limit(limit)
    if only_active:
        query = query.where(Product.is_active == True)
    result = await db.execute(query.order_by(Product.created_at.desc()))
    product = result.scalars().all()
    return product

    """Get featured products - returns products with stock > 0"""

async def get_featured_products(db: AsyncSession, limit: int = 10):
    result = await db.execute(
        select(Product).where(Product.stock > 0).limit(limit)
    )
    products = result.scalars().all()
    return products
