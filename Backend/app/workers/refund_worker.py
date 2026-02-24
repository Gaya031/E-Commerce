from app.services.refund_service import process_refund


async def refund_worker(order_id: int):
    await process_refund(order_id)
