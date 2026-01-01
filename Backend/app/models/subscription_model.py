from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    plan_name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    commission_percent = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    