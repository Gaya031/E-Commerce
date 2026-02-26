from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.seller_model import Seller
from app.models.product_model import Product
from app.utils.distance import calculate_distance_km
from app.utils.simple_cache import cache_get, cache_set
from typing import List, Optional


async def get_nearby_stores(
    db: AsyncSession,
    lat: float,
    lng: float,
    radius_km: float = 10.0,
    skip: int = 0,
    limit: int = 20
) -> List[dict]:
    """
    Get stores within a given radius of the user's location.
    Returns stores sorted by distance.
    """
    cache_key = f"stores:nearby:{round(lat,4)}:{round(lng,4)}:{radius_km}:{skip}:{limit}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    result = await db.execute(
        select(Seller)
        .where(Seller.approved == True)
        .where(Seller.latitude.is_not(None), Seller.longitude.is_not(None))
        .limit(1000)
    )
    sellers = result.scalars().all()
    
    stores_with_distance = []
    for seller in sellers:
        if seller.latitude and seller.longitude:
            try:
                seller_lat = float(seller.latitude)
                seller_lng = float(seller.longitude)
                distance = calculate_distance_km(lat, lng, seller_lat, seller_lng)
                
                if distance <= radius_km:
                    stores_with_distance.append({
                        "id": seller.id,
                        "store_name": seller.store_name,
                        "logo_url": seller.logo_url,
                        "description": seller.description,
                        "city": seller.city,
                        "distance_km": round(distance, 2),
                        "total_reviews": seller.total_reviews,
                        "average_rating": seller.average_rating,
                        "delivery_time_minutes": _estimate_delivery_time(distance)
                    })
            except (ValueError, TypeError):
                continue
    
    # Sort by distance and apply pagination after filtering.
    stores_with_distance.sort(key=lambda x: x["distance_km"])
    payload = stores_with_distance[skip : skip + limit]
    await cache_set(cache_key, payload, ttl_seconds=30)
    return payload


async def get_store_by_id(db: AsyncSession, store_id: int) -> Optional[Seller]:
    """Get a store by ID"""
    result = await db.execute(
        select(Seller).where(Seller.id == store_id)
    )
    return result.scalar_one_or_none()


async def get_store_products(
    db: AsyncSession,
    store_id: int,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> List[Product]:
    """Get all active products for a store"""
    query = select(Product).where(
        Product.seller_id == store_id,
        Product.is_active == True
    )
    
    if category:
        query = query.where(Product.category == category)
    
    query = query.offset(skip).limit(limit).order_by(Product.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_store_bestsellers(
    db: AsyncSession,
    store_id: int,
    limit: int = 10
) -> List[Product]:
    """Get bestsellers for a store (products with highest average rating and sales)"""
    result = await db.execute(
        select(Product)
        .where(
            Product.seller_id == store_id,
            Product.is_active == True,
            Product.average_rating > 0
        )
        .order_by(Product.average_rating.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_store_by_user_id(db: AsyncSession, user_id: int) -> Optional[Seller]:
    """Get seller profile by user ID"""
    result = await db.execute(
        select(Seller).where(Seller.user_id == user_id)
    )
    return result.scalar_one_or_none()


def _estimate_delivery_time(distance_km: float) -> int:
    """
    Estimate delivery time in minutes based on distance.
    Assumes average speed of 20 km/h for urban delivery.
    """
    # Base time for preparation: 15 minutes
    # Travel time: distance / speed * 60
    travel_time = (distance_km / 20) * 60
    total_time = int(15 + travel_time)
    return min(total_time, 120)  # Cap at 2 hours
