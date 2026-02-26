from pydantic import BaseModel
from typing import Optional

class PaymentInitiate(BaseModel):
    order_id: int
    
class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    payment_id: Optional[int] = None


class PaymentConfirm(BaseModel):
    payment_id: int
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None

class RefundRequest(BaseModel):
    order_id: int
    reason: Optional[str]
    
