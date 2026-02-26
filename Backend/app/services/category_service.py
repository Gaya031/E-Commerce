from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.category_model import Category
from app.models.product_model import Product


async def create_category(db: AsyncSession, data: dict):
    """Create a new category"""
    category = Category(**data)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: int):
    """Get a category by ID"""
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    return result.scalar_one_or_none()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all active categories"""
    result = await db.execute(
        select(Category)
        .where(Category.is_active == True)
        .order_by(Category.display_order, Category.name)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_all_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all categories including inactive"""
    result = await db.execute(
        select(Category)
        .order_by(Category.display_order, Category.name)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_category_by_slug(db: AsyncSession, slug: str):
    """Get a category by slug"""
    result = await db.execute(
        select(Category).where(Category.slug == slug)
    )
    return result.scalar_one_or_none()


async def update_category(db: AsyncSession, category_id: int, data: dict):
    """Update a category"""
    category = await get_category(db, category_id)
    if not category:
        return None
    
    for key, value in data.items():
        if value is not None:
            setattr(category, key, value)
    
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int):
    """Soft delete a category (set is_active to False)"""
    category = await get_category(db, category_id)
    if not category:
        return False
    
    category.is_active = False
    await db.commit()
    return True


async def get_subcategories(db: AsyncSession, parent_id: int):
    """Get subcategories of a parent category"""
    result = await db.execute(
        select(Category)
        .where(Category.parent_id == parent_id, Category.is_active == True)
        .order_by(Category.display_order, Category.name)
    )
    return result.scalars().all()


async def get_category_products(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 50):
    category = await get_category(db, category_id)
    if not category:
        return []

    result = await db.execute(
        select(Product)
        .where(
            Product.is_active == True,
            or_(
                Product.category.ilike(category.name),
                Product.category.ilike(category.slug),
            ),
        )
        .order_by(Product.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
