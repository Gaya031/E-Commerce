from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth_deps import require_roles
from app.core.exceptions import NotFoundException
from app.db.postgres import get_db
from app.models.product_model import Product
from app.models.seller_model import Seller
from app.models.user_model import User
from app.schemas.product_schema import ProductCreate, ProductOut, ProductUpdate, StockUpdate
from app.services.product_service import (
    create_product,
    delete_product,
    get_featured_products,
    get_products,
    update_product,
    update_stock,
)

router = APIRouter(tags=["products"])


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    return await create_product(db=db, user_id=seller.id, data=data.model_dump())


@router.put("/{product_id}", response_model=ProductOut)
async def update(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    return await update_product(
        db=db,
        product_id=product_id,
        user_id=seller.id,
        data=data.model_dump(exclude_none=True),
    )


@router.patch("/{product_id}/stock", response_model=ProductOut)
async def update_product_stock(
    product_id: int,
    data: StockUpdate,
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    return await update_stock(db=db, product_id=product_id, user_id=seller.id, new_stock=data.stock)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    await delete_product(db=db, product_id=product_id, user_id=seller.id)


@router.get("/", response_model=list[ProductOut], status_code=status.HTTP_200_OK)
async def products(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    include_inactive: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    skip = (page - 1) * size
    return await get_products(db=db, skip=skip, limit=size, only_active=not include_inactive)


@router.get("/mine", response_model=list[ProductOut])
async def my_products(
    db: AsyncSession = Depends(get_db),
    seller: User = Depends(require_roles("seller")),
):
    seller_result = await db.execute(select(Seller).where(Seller.user_id == seller.id))
    seller_profile = seller_result.scalars().first()
    if not seller_profile:
        return []
    result = await db.execute(select(Product).where(Product.seller_id == seller_profile.id))
    return result.scalars().all()


@router.get("/featured", response_model=list[ProductOut])
async def featured_products(db: AsyncSession = Depends(get_db)):
    return await get_featured_products(db=db)


@router.get("/search", response_model=list[ProductOut])
async def search_products(
    q: str = Query(..., min_length=1, max_length=120),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(
            or_(Product.title.ilike(f"%{q}%"), Product.description.ilike(f"%{q}%"))
        )
    )
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise NotFoundException("Product not found")
    return product
