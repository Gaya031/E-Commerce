from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

