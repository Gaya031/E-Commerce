from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class SellerCreate(BaseModel):
    store_name: str = Field(min_length=3)
    
class SellerKYCUpdate(BaseModel):
    aadhar: Optional[str]
    pan: Optional[str]
    gst: Optional[str]
    business_proof: Optional[str]

class SellerOut(BaseModel):
    id: int
    user_id: int
    store_name: str
    approved: bool
    commission_percent: int
    subscription_plan_id: Optional[int]
    subscription_expiry: Optional[datetime]
    kyc_docs: Optional[Dict]
    
    class Config: 
        from_attributes = True

