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
    
    class Config: 
        from_attributes = True
        