from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime


class StoreBase(BaseModel):
    store_name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_image: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    delivery_radius_km: int = 5


class StoreOut(StoreBase):
    id: int
    user_id: int
    approved: bool
    total_reviews: int = 0
    average_rating: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True


class NearbyStoreResponse(BaseModel):
    id: int
    store_name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    distance_km: float
    total_reviews: int = 0
    average_rating: float = 0.0
    delivery_time_minutes: Optional[int] = None


if TYPE_CHECKING:
    from app.schemas.product_schema import ProductOut


class StoreProductsResponse(BaseModel):
    store: StoreOut
    products: List["ProductOut"] = []
