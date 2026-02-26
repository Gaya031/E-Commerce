import enum
from sqlalchemy import (Column, Integer, String, Enum, ForeignKey, DateTime, func)
from app.db.base import Base

class PaymentStatus(str, enum.Enum):
    initiated = "initiated"
    completed = "completed"
    refunded = "refunded"
    failed = "failed"
    
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    razorpay_order_id = Column(String, nullable=True, index=True)
    razorpay_payment_id = Column(String, nullable=True, index=True)
    razorpay_refund_id = Column(String, nullable=True, index=True)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.initiated)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
