from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order_model import Order, PaymentMethod
from app.models.order_item_model import OrderItem
from app.models.product_model import Product
from decimal import Decimal


async def create_order(
    db: AsyncSession,
    buyer_id: int,
    payload
):
    total = Decimal("0.00")
    order_items = []

    # Validate products & calculate total
    for item in payload.items:
        q = await db.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = q.scalars().first()

        if not product or not product.is_active:
            raise ValueError("Invalid product")

        total += Decimal(product.price) * item.quantity

        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )
        )

    # Create order
    order = Order(
        buyer_id=buyer_id,
        seller_id=payload.seller_id,
        total_amount=total,
        payment_method=PaymentMethod(payload.payment_method),
        address_snapshot=payload.address,
    )

    db.add(order)
    await db.flush()

    for oi in order_items:
        oi.order_id = order.id
        db.add(oi)

    await db.commit()
    await db.refresh(order)

    return order