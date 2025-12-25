from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.payout_model import Payout
from app.models.commission_model import Commission
from app.models.delivery_model import Delivery
from app.core.exceptions import ConflictException

async def create_seller_payout(db: AsyncSession, seller_id: int):
    commissions = await db.execute(
        select(Commission).where(
            Commission.seller_id == seller_id
        )
    )
    rows = commissions.scalars().all()
    
    if not rows: 
        raise ConflictException("No earnings to payout")
    
    total = sum(row.seller_earning for row in rows)
    
    payout = Payout(
        user_id = seller_id,
        amount = total,
        payout_type = "seller",
        reference_ids = ",".join(str(r.order_id) for r in rows)
    )
    db.add(payout)
    await db.commit()
    return payout

async def create_delivery_payout(db: AsyncSession, partner_id: int):
    deliveries = await db.execute(
        select(Delivery).where(
            Delivery.partner_id == partner_id,
            Delivery.status == "delivered"
        )
    )
    rows = deliveries.scalars().all()
    
    if not rows:
        raise ConflictException("No earnings to payout")
    
    total = sum(row.partner_earning for row in rows)
    
    payout = Payout(
        user_id = partner_id,
        amount = total,
        payout_type = "delivery",
        reference_ids = ",".join(str(r.id) for r in rows)
    ) 
    
    db.add(payout)
    await db.commit()
    return payout