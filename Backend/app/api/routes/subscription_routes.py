from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.subscription_schema import (SubsciptionOut, SubscriptionCreate)
from app.services.subscription_service import (
    activate_seller_subscription,
    create_subscription,
    list_active_subscriptions,
)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubsciptionOut)
async def admin_create_subscription(data: SubscriptionCreate, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await create_subscription(db, data)

@router.get("/", response_model=list[SubsciptionOut])
async def list_plans(db: AsyncSession = Depends(get_db)):
    return await list_active_subscriptions(db)


@router.post("/activate/{plan_id}")
async def activate_plan_for_seller(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    profile = await activate_seller_subscription(db=db, user_id=seller.id, plan_id=plan_id)
    return {
        "seller_id": profile.id,
        "subscription_plan_id": profile.subscription_plan_id,
        "subscription_expiry": profile.subscription_expiry.isoformat() if profile.subscription_expiry else None,
        "commission_percent": profile.commission_percent,
    }

