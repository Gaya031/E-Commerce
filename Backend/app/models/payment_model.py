import enum
from sqlalchemy import (Column, Integer, String, Enum, ForeignKey, DateTime, func)
from app.db.base import Base

class PaymentStatus(str, enum.Enum):
    intiated = "initiated"
    completed = "completed"
    refunded = "refunded"
    failed = "failed"
    
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    razorpay_order_id = Column(String, nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    razorpay_refund_id = Column(String, nullable=True)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.intiated)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    