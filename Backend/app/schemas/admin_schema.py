from pydantic import BaseModel
from typing import Optional

class SellerApproval(BaseModel):
    approved: bool
    commission_percent: Optional[int]
    
class UserBlock(BaseModel):
    blocked: bool
    
class ReturnDecision(BaseModel):
    approved: bool

