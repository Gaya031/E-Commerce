from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.postgres import get_db
from app.schemas.store_schema import NearbyStoreResponse, StoreOut
from app.services import store_service
from app.models.product_model import Product
from app.schemas.product_schema import ProductOut
from app.models.seller_model import Seller

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/nearby", response_model=list[NearbyStoreResponse])
async def get_nearby_stores(
    lat: float = Query(..., description="User's latitude"),
    lng: float = Query(..., description="User's longitude"),
    radius_km: float = Query(10.0, ge=0.5, le=50, description="Search radius in km"),
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get nearby stores based on user's location.
    Returns stores sorted by distance from the user.
    """
    skip = (page - 1) * size
    stores = await store_service.get_nearby_stores(
        db=db,
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        skip=skip,
        limit=size
    )
    return stores


@router.get("/{store_id}", response_model=StoreOut)
async def get_store_details(
    store_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific store"""
    store = await store_service.get_store_by_id(db=db, store_id=store_id)
    if not store:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.get("/{store_id}/products", response_model=list[ProductOut])
async def get_store_products(
    store_id: int,
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    size: int = Query(50, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all products for a specific store"""
    # Verify store exists
    store = await store_service.get_store_by_id(db=db, store_id=store_id)
    if not store:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Store not found")
    
    skip = (page - 1) * size
    products = await store_service.get_store_products(
        db=db,
        store_id=store_id,
        category=category,
        skip=skip,
        limit=size
    )
    return products


@router.get("/{store_id}/bestsellers", response_model=list[ProductOut])
async def get_store_bestsellers(
    store_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get bestseller products from a specific store"""
    # Verify store exists
    store = await store_service.get_store_by_id(db=db, store_id=store_id)
    if not store:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Store not found")
    
    products = await store_service.get_store_bestsellers(
        db=db,
        store_id=store_id,
        limit=limit
    )
    return products
