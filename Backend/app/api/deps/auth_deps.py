from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.postgres import get_db
from app.models.user_model import User
from app.core.security import get_current_user_id


async def get_current_user(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if user.is_blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
    
    return user

def require_roles(*roles: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {roles}",
            )
        return current_user
    return role_checker

