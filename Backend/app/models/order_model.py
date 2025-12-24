import enum
from sqlalchemy import (Column, Integer, Enum, ForeignKey, Boolean, DateTime, Text, func)
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class OrderStatus(str, enum.Enum):
    placed = "placed"
    packed = "packed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    
class PaymentMethod(str, enum.Enum):
    prepaid = "prepaid"
    cod = "cod"
    
class ReturnStatus(str, enum.Enum):
    none = "none"
    requested = "requested"
    approved = "approved"
    picked = "picked"
    rejected = "rejected"
    
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.placed)
    address = Column(JSONB, nullable=False)
    is_returned = Column(Boolean, default=False)
    return_status = Column(Enum(ReturnStatus), default=ReturnStatus.none)
    return_reason = Column(Text)
    return_image = Column(Text)
    
    delivery_partner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_picked = Column(Boolean, default=False)
    commission_amount = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    