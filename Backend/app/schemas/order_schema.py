from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from app.models.order_model  import OrderStatus, PaymentMethod

class CartItemIn(BaseModel):
    product_id: int
    quantity: int
    
class AddressSchema(BaseModel):
    name: str
    phone: str
    house_no: str
    city: str
    state: str
    pincode: str
    coordinates: Optional[Dict] = None
    delivery_mode: Optional[str] = "instant"
    
class OrderCreate(BaseModel):
    seller_id: int
    items: List[CartItemIn]
    address: AddressSchema
    payment_method: PaymentMethod
    
class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    
class ReturnRequest(BaseModel):
    reason: str
    image: Optional[str]
    
class OrderOut(BaseModel):
    order_id: int
    status: str
    total_amount: float
