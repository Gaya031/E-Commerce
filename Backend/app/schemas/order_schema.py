from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from app.models.order_model  import OrderStatus, PaymentMethod

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    
class AddressSchema(BaseModel):
    name: str
    phone: str
    house_no: str
    city: str
    state: str
    pincode: str
    coordinates: Optional[Dict]
    
class OrderCreate(BaseModel):
    seller_id: int
    items: List[OrderItemCreate]
    address: AddressSchema
    payment_method: PaymentMethod
    
class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    
class ReturnRequest(BaseModel):
    reason: str
    image: Optional[str]
    