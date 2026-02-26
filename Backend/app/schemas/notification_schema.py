from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.notification_model import NotificationType


class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    message: str
    type: NotificationType = NotificationType.system
    link: Optional[str] = None


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
