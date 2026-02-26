from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, func
from app.db.base import Base
import enum


class NotificationType(str, enum.Enum):
    order = "order"
    payment = "payment"
    delivery = "delivery"
    promotion = "promotion"
    system = "system"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.system)
    is_read = Column(Boolean, default=False)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
