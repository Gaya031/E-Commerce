from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.utils.rate_limiter import RateLimiter
from app.services.search_service import (
    global_search as global_search_service,
    search_products as search_products_service,
    search_stores as search_stores_service,
)

search_rate_limit = RateLimiter(limit=60, window_seconds=60, key_prefix="search")
router = APIRouter(prefix="/search", tags=["search"], dependencies=[Depends(search_rate_limit)])


@router.get("/")
async def global_search(
    q: str = Query(..., min_length=1, max_length=120),
    db: AsyncSession = Depends(get_db)
):
    """Global search across products and stores"""
    return await global_search_service(db=db, q=q)


@router.get("/products")
async def search_products(
    q: str = Query(..., min_length=1, max_length=120),
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search products by name or description"""
    return await search_products_service(db=db, q=q, page=page, size=size)


@router.get("/stores")
async def search_stores(
    q: str = Query(..., min_length=1, max_length=120),
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search stores by name or description"""
    return await search_stores_service(db=db, q=q, page=page, size=size)
