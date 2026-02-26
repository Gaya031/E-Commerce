from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import get_current_user
from app.db.postgres import get_db
from app.models.user_model import User
from app.schemas.review_schema import ReviewCreate, ReviewOut
from app.services.review_service import (
    create_review,
    delete_review_by_owner,
    get_product_review_summary,
    get_store_review_summary,
    list_product_reviews,
    list_store_reviews,
)
from app.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/reviews", tags=["reviews"])
review_rate_limit = RateLimiter(limit=15, window_seconds=300, key_prefix="reviews")


@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def submit_review(
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _rate_limit: None = Depends(review_rate_limit),
):
    return await create_review(
        db=db, buyer_id=user.id, product_id=data.product_id, rating=data.rating, comment=data.comment
    )


@router.get("/product/{product_id}", response_model=list[ReviewOut])
async def product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * size
    return await list_product_reviews(db=db, product_id=product_id, skip=skip, limit=size)


@router.get("/store/{store_id}", response_model=list[ReviewOut])
async def store_reviews(
    store_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * size
    return await list_store_reviews(db=db, store_id=store_id, skip=skip, limit=size)


@router.get("/product/{product_id}/summary")
async def product_review_summary(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_review_summary(db=db, product_id=product_id)


@router.get("/store/{store_id}/summary")
async def store_review_summary(store_id: int, db: AsyncSession = Depends(get_db)):
    return await get_store_review_summary(db=db, store_id=store_id)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    deleted = await delete_review_by_owner(db=db, review_id=review_id, buyer_id=user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
