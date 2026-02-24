from pydantic import BaseModel
from typing import Optional

class PaymentInitiate(BaseModel):
    order_id: int
    
class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

class RefundRequest(BaseModel):
    order_id: int
    reason: Optional[str]
    
