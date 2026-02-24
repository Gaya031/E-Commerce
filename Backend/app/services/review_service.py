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
    await db.commit()
    await db.refresh(review)
    
    avg_rating = await db.execute(
        select(func.avg(Review.rating)).where(
            Review.product_id == product_id
        )
    )
    product = await db.get(Product, product_id)
    product.average_rating = int(avg_rating.scalar() or 0)
    await db.commit()
    
    return review

