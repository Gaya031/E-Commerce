from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.user_schema import UserOut
from app.services.user_service import list_users
from app.api.deps.auth_deps import get_current_user, require_roles
from app.models.user_model import User

router = APIRouter( tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_my_profile(user: User = Depends(get_current_user)):
    return user

@router.get("/", response_model=list[UserOut])
async def admin_list_users(page: int = Query(1, ge=1), size: int = Query(20, le=100), db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await list_users(db, page, size)
