from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import UserCreate, UserOut, TokenPair
from app.db.postgres import get_db
from app.services.auth_service import create_user, authenticate_user, create_tokens_for_user, refresh_access_token, logout_user, get_user_by_email
from app.utils.hashing import verify_password
from sqlalchemy import select
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_in)
    return user

@router.post("/login", response_model=TokenPair)
async def login(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access, refresh = await create_tokens_for_user(db, user)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenPair)
async def refersh(tokens: dict, db: AsyncSession = Depends(get_db)):
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    access, new_refresh = await refresh_access_token(db, refresh_token)
    if not access: raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"access_token": access, "refresh_token": new_refresh, "token_type": "bearer"}

@router.post("/logout", status_code=204)
async def logout(payload: dict, db: AsyncSession = Depends(get_db)):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await logout_user(db, user)
    return None