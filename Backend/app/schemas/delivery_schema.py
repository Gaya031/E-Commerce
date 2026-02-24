from pydantic import BaseModel
from typing import Optional, Dict
from app.models.delivery_model import DeliveryStatus

class DeliveryAssign(BaseModel):
    order_id: int
    partner_id: int
    distance_km: int
    
class DeliveryStatusUpdate(BaseModel):
    status: DeliveryStatus
    
class LocationPing(BaseModel):
    order_id: int
    coordinates: Dict
