from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from app.models.notification_model import Notification


async def create_notification(db: AsyncSession, user_id: int, data: dict, auto_commit: bool = True):
    """Create a new notification"""
    notification = Notification(user_id=user_id, **data)
    db.add(notification)
    if auto_commit:
        await db.commit()
        await db.refresh(notification)
    return notification


async def get_user_notifications(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20):
    """Get notifications for a user"""
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_unread_count(db: AsyncSession, user_id: int):
    """Get count of unread notifications"""
    result = await db.execute(
        select(func.count(Notification.id))
        .where(Notification.user_id == user_id, Notification.is_read == False)
    )
    return result.scalar()


async def mark_as_read(db: AsyncSession, notification_id: int, user_id: int):
    """Mark a notification as read"""
    result = await db.execute(
        select(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    notification = result.scalar_one_or_none()
    if notification:
        notification.is_read = True
        await db.commit()
        await db.refresh(notification)
    return notification


async def mark_all_as_read(db: AsyncSession, user_id: int):
    """Mark all notifications as read for a user"""
    result = await db.execute(
        update(Notification)
        .where(Notification.user_id == user_id, Notification.is_read == False)
        .values(is_read=True)
    )
    await db.commit()
    return result.rowcount or 0


async def delete_notification(db: AsyncSession, notification_id: int, user_id: int):
    """Delete a notification"""
    result = await db.execute(
        delete(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    await db.commit()
    return (result.rowcount or 0) > 0
