from app.services.refund_service import process_refund
from app.db.postgres import AsyncSessionLocal


async def refund_worker(order_id: int):
    async with AsyncSessionLocal() as db:
        await process_refund(db=db, order_id=order_id)
