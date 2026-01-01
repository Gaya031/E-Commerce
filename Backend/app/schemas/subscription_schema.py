from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    plan_name: str
    price: int
    commission_percent: int
    duration_days: int
    
class SubsciptionOut(BaseModel):
    id: int
    plan_name: str
    price: int
    commission_percent: int
    duration_days: int
    active: bool
    
    class Config: 
        from_attributes = True
        
