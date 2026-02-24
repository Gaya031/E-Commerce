from pydantic import BaseModel

class CommissionOut(BaseModel):
    order_id: int
    seller_id: int
    commission_percent: int
    commission_amount: int
    seller_earning: int
    platform_earning: int
    
    class Config: 
        from_attributes = True