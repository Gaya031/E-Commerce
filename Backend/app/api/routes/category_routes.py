from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from app.schemas.product_schema import ProductOut
from app.services.category_service import (
    create_category,
    get_category,
    get_categories,
    get_all_categories,
    get_category_by_slug,
    update_category,
    delete_category,
    get_subcategories,
    get_category_products,
)
from app.api.deps.auth_deps import get_current_user, require_roles
from app.models.user_model import User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    """Create a new category (admin only)"""
    return await create_category(db=db, data=data.model_dump())


@router.get("/", response_model=list[CategoryOut])
async def list_categories(
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get all active categories"""
    skip = (page - 1) * size
    return await get_categories(db=db, skip=skip, limit=size)


@router.get("/all", response_model=list[CategoryOut])
async def list_all_categories(
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    """Get all categories including inactive (admin only)"""
    skip = (page - 1) * size
    return await get_all_categories(db=db, skip=skip, limit=size)


@router.get("/slug/{slug}", response_model=CategoryOut)
async def get_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a category by slug"""
    category = await get_category_by_slug(db=db, slug=slug)
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/{category_id}", response_model=CategoryOut)
async def get(category_id: int, db: AsyncSession = Depends(get_db)):
    """Get a category by ID"""
    category = await get_category(db=db, category_id=category_id)
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryOut)
async def update(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    """Update a category (admin only)"""
    category = await update_category(
        db=db,
        category_id=category_id,
        data=data.model_dump(exclude_none=True)
    )
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    """Soft delete a category (admin only)"""
    success = await delete_category(db=db, category_id=category_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")


@router.get("/{category_id}/subcategories", response_model=list[CategoryOut])
async def list_subcategories(category_id: int, db: AsyncSession = Depends(get_db)):
    """Get subcategories of a category"""
    return await get_subcategories(db=db, parent_id=category_id)


@router.get("/{category_id}/products", response_model=list[ProductOut])
async def list_category_products(
    category_id: int,
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Get active products for a category"""
    skip = (page - 1) * size
    return await get_category_products(db=db, category_id=category_id, skip=skip, limit=size)
