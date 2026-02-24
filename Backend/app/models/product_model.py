from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, Text, DateTime, func)
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    seller_id = Column(
        Integer,
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    images = Column(JSONB, nullable=True)
    category = Column(String(100), index = True)
    is_active = Column(Boolean, default=True)
    average_rating = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    