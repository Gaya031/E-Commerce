from app.db.redis import get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.utils.hashing import get_password_hashed, verify_password
from app.utils.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.schemas.auth_schema import UserCreate
from typing import Tuple, Optional
import jwt

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalars().first()

async def create_user(db: AsyncSession, user_in:UserCreate) -> User:
    hashed = get_password_hashed(user_in.password)
    user = User(
        name=user_in.name,
        email=user_in.email,
        phone=user_in.phone,
        password=hashed,
        role=user_in.role,
        refresh_token=None
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

async def create_tokens_for_user(db: AsyncSession, user: User) -> Tuple[str, str]:
    redis = await get_redis()
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    
    await redis.set(f"refresh:{user.id}", refresh, ex=60*60*24*7)
    # user.refresh_token = refresh
    # db.add(user)
    # await db.commit()
    return access, refresh

async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        payload = decode_token(refresh_token)
        user_id = int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        return None, None
    except Exception: 
        return None, None
    
    redis = await get_redis()
    stored = await redis.get(f"refresh:{user_id}")
    if stored != refresh_token:
        return None, None
    
    
    new_access = create_access_token(user_id)
    new_refersh = create_refresh_token(user_id)
    await redis.set(f"refresh:{user_id}", new_refersh, ex=60*60*24*7)
    return new_access, new_refersh

async def logout_user(db: AsyncSession, user: User):
    redis = await get_redis()
    await redis.delete(f"refresh:{user.id}")
    return True