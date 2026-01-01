from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user_model import UserRole

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    password: str = Field(min_length=8)
    role: UserRole = UserRole.buyer

class UserIn(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    wallet_balance: int
    
    class Config:
        from_attributes = True

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    sub: int
    exp: int
    