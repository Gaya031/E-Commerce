from sqlalchemy import (Column, Integer, ForeignKey, Text, DateTime, func)
from app.db.base import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key = True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    buyer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    rating = Column(Integer, nullable=False) # 1 - 5
    comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    