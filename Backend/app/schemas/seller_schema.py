from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class SellerCreate(BaseModel):
    store_name: str = Field(min_length=3)
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    logo_url: Optional[str] = None
    cover_image: Optional[str] = None
    delivery_radius_km: Optional[int] = Field(default=5, ge=1, le=50)

class SellerUpdate(BaseModel):
    store_name: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    logo_url: Optional[str] = None
    cover_image: Optional[str] = None
    delivery_radius_km: Optional[int] = Field(default=None, ge=1, le=50)
    
class SellerKYCUpdate(BaseModel):
    aadhar: Optional[str] = None
    pan: Optional[str] = None
    gst: Optional[str] = None
    business_proof: Optional[str] = None

class SellerOut(BaseModel):
    id: int
    user_id: int
    store_name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_image: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    delivery_radius_km: int = 5
    total_reviews: int = 0
    average_rating: float = 0.0
    approved: bool
    commission_percent: int
    subscription_plan_id: Optional[int] = None
    subscription_expiry: Optional[datetime] = None
    kyc_docs: Optional[Dict] = None
    
    class Config: 
        from_attributes = True

