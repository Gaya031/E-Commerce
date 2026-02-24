from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.core.exceptions import NotFoundException

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException("user not found")
    return user

async def update_user_location(db: AsyncSession, user_id: int, location_data: dict) -> User:
    user = await get_user_by_id(db, user_id)
    for key, value in location_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

async def list_users(db: AsyncSession, page: int = 1, size: int = 20):
    offset = (page - 1) * size
    result = await db.execute(select(User).offset(offset).limit(size))
    return result.scalars().all()

