from sqlalchemy import (Column, Integer, ForeignKey, String, DateTime, func)
from app.db.base import Base

class Payout(Base):
    __tablename__ = "payouts"
    
    id = Column(Integer, primary_key = True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    amount = Column(Integer, nullable=False)
    payout_type = Column(String, nullable= False) # seller/delivery
    reference_ids = Column(String) #order_ids or delivery_ids
    status = Column(String, default="pending") # pending, completed, failed
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )