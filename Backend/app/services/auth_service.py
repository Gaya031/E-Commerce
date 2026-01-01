from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis.asyncio import Redis
from app.models.user_model import User
from app.schemas.auth_schema import UserCreate
from app.utils.hashing import get_password_hashed, verify_password
from app.utils.jwt_handler import (create_access_token, create_refresh_token, decode_token)
from app.core.exceptions import(AuthException, NotFoundException)
from app.db.redis import get_redis

REFRESH_TOKEN_TTL = 60*60*24*7

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    print(f"email got:{email}")
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        name = user_in.name,
        email = user_in.email,
        phone = user_in.phone,
        password = get_password_hashed(user_in.password),
        role = user_in.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    print("email recieved")
    print(email)
    user = await get_user_by_email(db, email)
    if not user:
        raise AuthException("Invalid email from password from user block")
    if not verify_password(password, user.password):
        raise AuthException("invalid email or password from password block")
    if user.is_blocked:
        raise AuthException("User is Blocked")
    return user

async def create_tokens_for_user(db: AsyncSession, user: User) -> Tuple[str, str]:
    redis: Redis = await get_redis()
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    await redis.set(
        f"refresh:{user.id}",
        refresh_token,
        ex=REFRESH_TOKEN_TTL
    )
    return access_token, refresh_token

async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
    except ValueError: 
        raise AuthException("Invalid or Expired refresh token")
    if payload.get("type") != "refresh":
        raise AuthException("Invalid token type")
    
    user_id = int(payload["sub"])
    redis: Redis = await get_redis()
    stored_token = await redis.get(f"refresh:{user_id}")
    
    if not stored_token or stored_token != refresh_token:
        raise AuthException("Refresh token revoked")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise NotFoundException("User not found")
    
    new_access = create_access_token(user.id)
    new_refresh = create_refresh_token(user.id)
    
    await redis.set(
        f"refresh: {user.id}",
        new_refresh,
        ex=REFRESH_TOKEN_TTL
    )
    return new_access, new_refresh

async def logout_user(user: User) -> None:
    redis: Redis = await get_redis()
    await redis.delete(f"refresh:{user.id}")
