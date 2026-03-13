from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.seller_model import Seller
from app.core.exceptions import ConflictException, NotFoundException, PermissionDeniedException
from app.core.logging import logger
from app.services.search_service import upsert_store_document
from app.utils.simple_cache import cache_delete_prefix


def _normalize_location_fields(data: dict | None) -> dict:
    if not data:
        return {}
    normalized = dict(data)
    for key in ("latitude", "longitude"):
        if key in normalized and normalized[key] is not None:
            try:
                normalized[key] = float(normalized[key])
            except (TypeError, ValueError):
                normalized[key] = None
    return normalized


async def create_seller_profile(
    db: AsyncSession, user_id: int, store_name: str, data: dict | None = None
) -> Seller:
    existing = await db.execute(select(Seller).where(Seller.user_id == user_id))
    if existing.scalars().first():
        raise ConflictException("Seller profile already exists")
    
    seller = Seller(
        user_id=user_id,
        store_name=store_name,
        approved=False,
        **_normalize_location_fields(data),
    )
    
    db.add(seller)
    await db.commit()
    await db.refresh(seller)
    try:
        await upsert_store_document(db, seller.id)
    except Exception as exc:
        logger.warning("Seller indexing failed for %s: %s", seller.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller


async def get_seller_by_user_id(db: AsyncSession, user_id: int) -> Seller | None:
    result = await db.execute(select(Seller).where(Seller.user_id == user_id))
    return result.scalars().first()


async def update_seller_profile(db: AsyncSession, user_id: int, data: dict) -> Seller:
    seller = await get_seller_by_user_id(db, user_id)
    if not seller:
        raise NotFoundException("Seller not found")

    normalized_data = _normalize_location_fields(data)
    for key, value in normalized_data.items():
        setattr(seller, key, value)

    await db.commit()
    await db.refresh(seller)
    try:
        await upsert_store_document(db, seller.id)
    except Exception as exc:
        logger.warning("Seller indexing failed for %s: %s", seller.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller


async def upload_kyc_for_user(db: AsyncSession, user_id: int, kyc_data: dict) -> Seller:
    seller = await get_seller_by_user_id(db, user_id)
    if not seller:
        raise NotFoundException("Seller not found")

    seller.kyc_docs = kyc_data
    await db.commit()
    await db.refresh(seller)
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller


async def upload_kyc_document_for_user(
    db: AsyncSession, user_id: int, doc_type: str, doc_url: str
) -> Seller:
    seller = await get_seller_by_user_id(db, user_id)
    if not seller:
        raise NotFoundException("Seller not found")

    docs = seller.kyc_docs if isinstance(seller.kyc_docs, dict) else {}
    docs = dict(docs)
    docs[doc_type] = doc_url
    seller.kyc_docs = docs

    await db.commit()
    await db.refresh(seller)
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller

async def upload_kyc(db: AsyncSession, seller_id: int, kyc_data: dict, user_id: int) -> Seller:
    result = await db.execute(select(Seller).where(Seller.id == seller_id))
    seller = result.scalars().first()
    
    if not seller:
        raise NotFoundException("Seller not found")
    
    if seller.user_id != user_id:
        raise PermissionDeniedException("Not your seller profile")
    
    seller.kyc_docs = kyc_data
    await db.commit()
    await db.refresh(seller)
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller

async def approve_seller(db: AsyncSession, seller_id: int, commission_percent: int) -> Seller:
    result = await db.execute(select(Seller).where(Seller.id == seller_id))
    seller = result.scalars().first()
    
    if not seller:
        raise NotFoundException("seller not found")
    
    seller.approved = True
    seller.commission_percent = commission_percent
    await db.commit()
    await db.refresh(seller)
    try:
        await upsert_store_document(db, seller.id)
    except Exception as exc:
        logger.warning("Seller indexing failed for %s: %s", seller.id, str(exc))
    await cache_delete_prefix("search:")
    await cache_delete_prefix("stores:")
    return seller
