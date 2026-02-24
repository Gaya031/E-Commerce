from pydantic import BaseModel
from typing import List

class WalletTransaction(BaseModel):
    amount: int
    type: str
    reference_id: str | None
    
    class Config:
        from_attributes = True
        
class WalletOut(BaseModel):
    balance: int
    transactions: List[WalletTransaction]
    