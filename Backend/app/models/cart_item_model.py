from sqlalchemy import Column, Integer, ForeignKey, String, Text, UniqueConstraint, DateTime, func
from app.db.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("buyer_id", "product_id", name="uq_cart_buyer_product"),)

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    store_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
