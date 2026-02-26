from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.review_model import Review
from app.models.order_item_model import OrderItem
from app.models.order_model import Order, OrderStatus
from app.models.product_model import Product
from app.core.exceptions import (ConflictException, PermissionDeniedException)

async def create_review(db: AsyncSession, buyer_id: int, product_id: int, rating: int, comment: str | None) -> Review:
    result = await db.execute(
        select(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .where(
            Order.buyer_id == buyer_id, 
            Order.status == OrderStatus.delivered,
            OrderItem.product_id == product_id
            )
        )
    if not result.scalars().first():
        raise PermissionDeniedException("You can only review purchased products")
    
    existing = await db.execute(
        select(Review).where(
            Review.buyer_id == buyer_id,
            Review.product_id == product_id
        )
    )
    
    if existing.scalars().first():
        raise ConflictException("Review already submitted")
    
    review = Review(
        buyer_id = buyer_id,
        product_id = product_id,
        rating = rating,
        comment = comment
    )
    db.add(review)
    await db.flush()
    
    avg_rating = await db.execute(
        select(func.avg(Review.rating)).where(
            Review.product_id == product_id
        )
    )
    product = await db.get(Product, product_id)
    product.average_rating = int(avg_rating.scalar() or 0)
    await db.commit()
    await db.refresh(review)
    return review


async def list_product_reviews(db: AsyncSession, product_id: int, skip: int = 0, limit: int = 20) -> list[Review]:
    result = await db.execute(
        select(Review)
        .where(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def list_store_reviews(db: AsyncSession, store_id: int, skip: int = 0, limit: int = 20) -> list[Review]:
    result = await db.execute(
        select(Review)
        .join(Product, Product.id == Review.product_id)
        .where(Product.seller_id == store_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_review_by_owner(db: AsyncSession, review_id: int, buyer_id: int) -> bool:
    result = await db.execute(select(Review).where(Review.id == review_id, Review.buyer_id == buyer_id))
    review = result.scalars().first()
    if not review:
        return False
    await db.delete(review)
    await db.commit()
    return True


async def get_product_review_summary(db: AsyncSession, product_id: int) -> dict:
    avg_and_count = await db.execute(
        select(
            func.coalesce(func.avg(Review.rating), 0).label("avg_rating"),
            func.count(Review.id).label("total_reviews"),
        ).where(Review.product_id == product_id)
    )
    row = avg_and_count.one()

    breakdown_rows = await db.execute(
        select(Review.rating, func.count(Review.id))
        .where(Review.product_id == product_id)
        .group_by(Review.rating)
    )
    breakdown = {int(rating): int(count) for rating, count in breakdown_rows.all()}
    for rating in range(1, 6):
        breakdown.setdefault(rating, 0)

    return {
        "average_rating": round(float(row.avg_rating or 0), 2),
        "total_reviews": int(row.total_reviews or 0),
        "breakdown": breakdown,
    }


async def get_store_review_summary(db: AsyncSession, store_id: int) -> dict:
    avg_and_count = await db.execute(
        select(
            func.coalesce(func.avg(Review.rating), 0).label("avg_rating"),
            func.count(Review.id).label("total_reviews"),
        )
        .join(Product, Product.id == Review.product_id)
        .where(Product.seller_id == store_id)
    )
    row = avg_and_count.one()

    breakdown_rows = await db.execute(
        select(Review.rating, func.count(Review.id))
        .join(Product, Product.id == Review.product_id)
        .where(Product.seller_id == store_id)
        .group_by(Review.rating)
    )
    breakdown = {int(rating): int(count) for rating, count in breakdown_rows.all()}
    for rating in range(1, 6):
        breakdown.setdefault(rating, 0)

    return {
        "average_rating": round(float(row.avg_rating or 0), 2),
        "total_reviews": int(row.total_reviews or 0),
        "breakdown": breakdown,
    }

