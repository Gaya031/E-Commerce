from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.commission_model import Commission
from app.models.delivery_model import Delivery, DeliveryStatus
from app.models.payout_model import Payout
from app.models.seller_model import Seller
from app.models.user_model import User, UserRole


def _parse_reference_ids(reference_ids: str | None) -> set[int]:
    if not reference_ids:
        return set()
    out: set[int] = set()
    for chunk in str(reference_ids).split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            out.add(int(chunk))
        except ValueError:
            continue
    return out


async def _resolve_seller(db: AsyncSession, seller_or_user_id: int) -> Seller | None:
    seller = await db.get(Seller, seller_or_user_id)
    if seller:
        return seller
    row = await db.execute(select(Seller).where(Seller.user_id == seller_or_user_id))
    return row.scalars().first()


async def create_seller_payout(db: AsyncSession, seller_id: int):
    seller = await _resolve_seller(db, seller_id)
    if not seller:
        return {"processed": False, "reason": "Seller profile not found"}

    paid_rows_result = await db.execute(
        select(Payout).where(Payout.payout_type == "seller", Payout.user_id == seller.user_id)
    )
    paid_rows = paid_rows_result.scalars().all()
    paid_order_ids = set()
    for payout in paid_rows:
        paid_order_ids.update(_parse_reference_ids(payout.reference_ids))

    commissions_result = await db.execute(select(Commission).where(Commission.seller_id == seller.id))
    rows = [row for row in commissions_result.scalars().all() if row.order_id not in paid_order_ids]

    if not rows:
        return {
            "processed": False,
            "reason": "No pending seller earnings to payout",
            "seller_id": seller.id,
            "seller_user_id": seller.user_id,
            "count": 0,
            "amount": 0,
        }

    total = int(sum(int(row.seller_earning or 0) for row in rows))
    reference_ids = ",".join(str(r.order_id) for r in rows)

    payout = Payout(
        user_id=seller.user_id,
        amount=total,
        payout_type="seller",
        reference_ids=reference_ids,
    )
    db.add(payout)
    await db.commit()
    await db.refresh(payout)
    return {
        "processed": True,
        "payout_id": payout.id,
        "seller_id": seller.id,
        "seller_user_id": seller.user_id,
        "amount": total,
        "count": len(rows),
        "reference_ids": reference_ids,
        "status": payout.status,
    }


async def create_delivery_payout(db: AsyncSession, partner_id: int):
    partner = await db.get(User, partner_id)
    if not partner or partner.role != UserRole.delivery:
        return {"processed": False, "reason": "Delivery partner not found"}

    paid_rows_result = await db.execute(
        select(Payout).where(Payout.payout_type == "delivery", Payout.user_id == partner.id)
    )
    paid_rows = paid_rows_result.scalars().all()
    paid_delivery_ids = set()
    for payout in paid_rows:
        paid_delivery_ids.update(_parse_reference_ids(payout.reference_ids))

    deliveries_result = await db.execute(
        select(Delivery).where(
            Delivery.partner_id == partner.id,
            Delivery.status == DeliveryStatus.delivered,
        )
    )
    rows = [row for row in deliveries_result.scalars().all() if row.id not in paid_delivery_ids]

    if not rows:
        return {
            "processed": False,
            "reason": "No pending delivery earnings to payout",
            "partner_id": partner.id,
            "count": 0,
            "amount": 0,
        }

    total = int(sum(int(row.partner_earning or 0) for row in rows))
    reference_ids = ",".join(str(r.id) for r in rows)

    payout = Payout(
        user_id=partner.id,
        amount=total,
        payout_type="delivery",
        reference_ids=reference_ids,
    )

    db.add(payout)
    await db.commit()
    await db.refresh(payout)
    return {
        "processed": True,
        "payout_id": payout.id,
        "partner_id": partner.id,
        "amount": total,
        "count": len(rows),
        "reference_ids": reference_ids,
        "status": payout.status,
    }
