import enum
from sqlalchemy import (Column, Integer, Enum, ForeignKey, DateTime, func)
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class DeliveryStatus(str, enum.Enum):
    assigned = "assigned"
    picked = "picked"
    delivered = "delivered"
    
class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key = True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable= False,
        unique=True
    )
    partner_id = Column(
        Integer, 
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    distance_km = Column(Integer)
    delivery_fee = Column(Integer)
    partner_earning = Column(Integer)
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.assigned)
    location_history = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    