from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.product_schema import (ProductCreate, ProductOut, ProductUpdate, StockUpdate)
from app.services.product_service import (create_product, update_product, update_stock, get_products)
from app.api.deps.auth_deps import require_roles
from app.models.user_model import User

router = APIRouter( tags=["products"])

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create(data: ProductCreate, db: AsyncSession = Depends(get_db), seller: User = Depends(require_roles("seller"))):
    return await create_product(db=db, user_id=seller.id, data=data.model_dump())


@router.put("/{product_id}", response_model=ProductOut)
async def update(product_id: int, data: ProductUpdate, db: AsyncSession = Depends(get_db), seller: User = Depends(require_roles("seller"))):
    return await update_product(db=db, product_id=product_id, user_id=seller.id, data=data.model_dump(exclude_none=True))

@router.patch("/{product_id}/stock", response_model=ProductOut)
async def update_product_stock(product_id: int, data: StockUpdate, db: AsyncSession = Depends(get_db), seller: User = Depends(require_roles("seller"))):
    return await update_stock(db=db, product_id=product_id, user_id=seller.id, new_stock=data.stock)

@router.get("/", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def products(db: AsyncSession = Depends(get_db)):
    return await get_products(db=db)