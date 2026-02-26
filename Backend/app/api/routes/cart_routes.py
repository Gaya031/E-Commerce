from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import get_current_user
from app.db.postgres import get_db
from app.models.user_model import User
from app.schemas.cart_schema import CartOut, CartSyncIn
from app.services.cart_service import clear_user_cart, get_user_cart, replace_user_cart, sync_guest_cart

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartOut)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await get_user_cart(db, user.id)


@router.put("/", response_model=CartOut)
async def replace_cart(
    payload: CartSyncIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await replace_user_cart(db, user.id, payload)


@router.post("/sync", response_model=CartOut)
async def sync_cart(
    payload: CartSyncIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await sync_guest_cart(db, user.id, payload)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await clear_user_cart(db, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
