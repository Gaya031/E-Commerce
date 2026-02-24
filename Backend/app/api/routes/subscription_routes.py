from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.subscription_schema import (SubsciptionOut, SubscriptionCreate)
from app.services.subscription_service import (create_subscription, list_active_subscriptions)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubsciptionOut)
async def admin_create_subscription(data: SubscriptionCreate, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await create_subscription(db, data)

@router.get("/", response_model=list[SubsciptionOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    return await list_active_subscriptions(db)

