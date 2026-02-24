from pydantic import BaseModel
from typing import List

class PayoutCreate(BaseModel):
    user_id: int
    amount: int
    payout_type: str
    reference_ids: List[int]
    
class Payout(BaseModel):
    id: int
    user_id: int
    amount: int
    payout_type: str
    status: str
    
    class Config: 
        from_attributes = True
        
