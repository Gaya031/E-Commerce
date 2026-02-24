from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.review_schema import ReviewCreate, ReviewOut
from app.services.review_service import create_review
from app.api.deps.auth_deps import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def submit_review(data: ReviewCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_review(db=db, buyer_id=user.id, product_id=data.product_id, rating=data.rating, comment=data.comment)

