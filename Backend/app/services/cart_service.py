from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart_item_model import CartItem
from app.schemas.cart_schema import CartSyncIn


def _serialize(items: list[CartItem]) -> dict:
    if not items:
        return {"store_id": None, "items": []}
    return {
        "store_id": items[0].store_id,
        "items": [
            {
                "product_id": i.product_id,
                "title": i.title,
                "price": i.price,
                "image": i.image,
                "quantity": i.quantity,
            }
            for i in items
        ],
    }


async def get_user_cart(db: AsyncSession, buyer_id: int) -> dict:
    q = await db.execute(select(CartItem).where(CartItem.buyer_id == buyer_id).order_by(CartItem.id.asc()))
    items = q.scalars().all()
    return _serialize(items)


async def replace_user_cart(db: AsyncSession, buyer_id: int, payload: CartSyncIn) -> dict:
    if payload.items and payload.store_id is None:
        raise HTTPException(status_code=400, detail="store_id is required when cart has items")

    await db.execute(delete(CartItem).where(CartItem.buyer_id == buyer_id))

    rows = []
    for item in payload.items:
        rows.append(
            CartItem(
                buyer_id=buyer_id,
                store_id=payload.store_id,
                product_id=item.product_id,
                title=item.title,
                price=item.price,
                image=item.image,
                quantity=item.quantity,
            )
        )

    if rows:
        db.add_all(rows)

    await db.commit()
    return await get_user_cart(db, buyer_id)


async def sync_guest_cart(db: AsyncSession, buyer_id: int, payload: CartSyncIn) -> dict:
    current = await get_user_cart(db, buyer_id)
    server_items = current["items"]
    server_store = current["store_id"]

    if not payload.items:
        return current

    if payload.store_id is None:
        raise HTTPException(status_code=400, detail="store_id is required when cart has items")

    if server_store and payload.store_id and server_store != payload.store_id:
        # Keep server cart authoritative if stores conflict.
        return current

    merged_store = server_store or payload.store_id
    merged_map = {item["product_id"]: {**item} for item in server_items}

    for item in payload.items:
        if item.product_id in merged_map:
            merged_map[item.product_id]["quantity"] += item.quantity
        else:
            merged_map[item.product_id] = {
                "product_id": item.product_id,
                "title": item.title,
                "price": item.price,
                "image": item.image,
                "quantity": item.quantity,
            }

    merged_payload = CartSyncIn(
        store_id=merged_store,
        items=[
            {
                "product_id": item["product_id"],
                "title": item["title"],
                "price": item["price"],
                "image": item["image"],
                "quantity": item["quantity"],
            }
            for item in merged_map.values()
        ],
    )

    return await replace_user_cart(db, buyer_id, merged_payload)


async def clear_user_cart(db: AsyncSession, buyer_id: int) -> None:
    await db.execute(delete(CartItem).where(CartItem.buyer_id == buyer_id))
    await db.commit()
