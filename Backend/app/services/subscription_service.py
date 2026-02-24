from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.subscription_model import Subscription
from app.core.exceptions import ConflictException
from app.schemas.subscription_schema import (SubscriptionCreate, SubsciptionOut)
async def create_subscription(db: AsyncSession, data: SubscriptionCreate) -> Subscription:
    exists = await db.execute(select(Subscription).where(Subscription.plan_name == data.plan_name))
    if exists.scalars().first():
        raise ConflictException("Sunscription already exists")
    sub = Subscription(**data.model_dump())
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

async def list_active_subscriptions(db: AsyncSession):
    result = await db.execute(select(Subscription).where(Subscription.active == True))
    return result.scalars().all()

