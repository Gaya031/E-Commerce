from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order_model import Order, OrderStatus, ReturnStatus
from app.models.order_item_model import OrderItem
from app.models.product_model import Product
from app.models.seller_model import Seller
from app.core.exceptions import PermissionDeniedException, NotFoundException, ConflictException

async def create_order(db: AsyncSession, buyer_id: int, data: dict) -> Order:
    seller = await db.execute(select(Seller).where(Seller.id == data["seller.id"]))
    seller = seller.scalars().first()
    if not seller or not seller.approved:
        raise PermissionDeniedException("Seller not available")
    
    total_amount = 0
    order_items = []
    
    for item in data["items"]:
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalars().first()
        
        if not product or product.is_active:
            raise NotFoundException("Product unavailable")
        
        if product.stock < item.quantity:
            raise ConflictException("Insufficient Stock")
        
        product.stock -= item.quantity
        total_amount += product.price * item.quantity
        
        order_items.append(
            OrderItem(
                product_id = product.id,
                quantity = item.quantity,
                price= product.price
            )
        )
        
    order = Order(
        buyer_id = buyer_id,
        seller_id = seller.id,
        total_amount = total_amount,
        payment_method = data["payment_method"],
        address = data["address"]
    )
    db.add(order)
    await db.flush()
    
    for item in order_items:
        item.order_id = order.id
        db.add(item)
    
    await db.commit()
    await db.refresh()
    return order


async def update_order_status(db: AsyncSession, order_id: int, user_id: int, new_status: OrderStatus) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    
    #Buyer can only cancel
    if new_status == OrderStatus.cancelled:
        if order.buyer_id != user_id:
            raise PermissionDeniedException("Not Allowed")
        
        if order.status != OrderStatus.placed:
            raise ConflictException("Cannot cancel now")
        
        order.status = OrderStatus.cancelled
        await db.commit()
        return order
    
    raise PermissionDeniedException("Invalid status transaction")


async def request_return(db: AsyncSession, order_id : int, buyer_id: int, reason: str, image: str | None):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    
    if not order or order.buyer_id != buyer_id:
        raise NotFoundException("Order not found")
    
    if order.status != OrderStatus.delivered:
        raise ConflictException("Return not allowed")
    
    order.is_returned = True
    order.return_status = ReturnStatus.requested
    order.return_reason = reason
    order.return_image = image
    
    await db.commit()
    return order

