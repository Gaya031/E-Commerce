from sqlalchemy import (Column, Integer, ForeignKey, DateTime, func)
from app.db.base import Base

class Commission(Base):
    __tablename__ = "commissions"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    seller_id = Column(
        Integer,
        ForeignKey("sellers.id"),
        nullable=False,
        index=True
    )
    commission_percent = Column(Integer, nullable=False)
    commission_amount = Column(Integer, nullable=False)
    seller_earning = Column(Integer, nullable=False)
    platform_earning = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    