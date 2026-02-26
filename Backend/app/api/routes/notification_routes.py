from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.notification_schema import NotificationCreate, NotificationUpdate, NotificationOut
from app.services.notification_service import (
    get_user_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_as_read,
    delete_notification
)
from app.api.deps.auth_deps import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=list[NotificationOut])
async def list_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get all notifications for the current user"""
    skip = (page - 1) * size
    return await get_user_notifications(db=db, user_id=user.id, skip=skip, limit=size)


@router.get("/unread-count")
async def unread_count(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Get count of unread notifications"""
    count = await get_unread_count(db=db, user_id=user.id)
    return {"unread_count": count}


@router.patch("/{notification_id}/read", response_model=NotificationOut)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Mark a notification as read"""
    notification = await mark_as_read(db=db, notification_id=notification_id, user_id=user.id)
    if not notification:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("/read-all")
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    count = await mark_all_as_read(db=db, user_id=user.id)
    return {"marked_read": count}


@router.delete("/{notification_id}", status_code=204)
async def delete_notification_route(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Delete a notification"""
    success = await delete_notification(db=db, notification_id=notification_id, user_id=user.id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Notification not found")
