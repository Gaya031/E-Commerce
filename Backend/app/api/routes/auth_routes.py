from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import (UserCreate, UserOut, TokenPair, UserIn)
from app.db.postgres import get_db
from app.services.auth_service import (create_user, authenticate_user, create_tokens_for_user, refresh_access_token, logout_user, get_user_by_email)
from app.api.deps.auth_deps import get_current_user
from app.models.user_model import User
from app.utils.rate_limiter import RateLimiter

router = APIRouter(prefix="/auth", tags=["auth"])

register_rate_limit = RateLimiter(limit=3, window_seconds=300, key_prefix="register")
@router.post("/register", dependencies=[Depends(register_rate_limit)], response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_in)
    return user


login_rate_limit = RateLimiter(limit=5, window_seconds=60, key_prefix="login")
@router.post("/login", dependencies=[Depends(login_rate_limit)], response_model=TokenPair)
async def login(data: UserIn, db: AsyncSession = Depends(get_db)):
    print("data recieved")
    user = await authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access, refresh = await create_tokens_for_user(db, user)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


refresh_rate_limit = RateLimiter(limit=10, window_seconds=300, key_prefix="refresh")
@router.post("/refresh", dependencies=[Depends(refresh_rate_limit)], response_model=TokenPair)
async def refresh(tokens: dict, db: AsyncSession = Depends(get_db)):
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    access, new_refresh = await refresh_access_token(db, refresh_token)
    if not access:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenPair(access_token=access, refresh_token=refresh )



@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: User = Depends(get_current_user)):
    await logout_user(current_user)