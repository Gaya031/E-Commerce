from pydantic import BaseModel, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    role: str
    wallet_balance: int
    is_blocked: bool
    # Location fields
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    
    class Config: 
        from_attributes = True

class UserLocationUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
        