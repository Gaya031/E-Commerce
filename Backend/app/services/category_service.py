from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category_model import Category
from app.models.product_model import Product


def _slugify(value: str | None) -> str:
    if not value:
        return ""
    text = value.strip().lower()
    out = []
    prev_dash = False
    for ch in text:
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        else:
            if not prev_dash:
                out.append("-")
                prev_dash = True
    slug = "".join(out).strip("-")
    return slug[:100]


def _name_from_slug(slug: str) -> str:
    if not slug:
        return ""
    return " ".join(part.capitalize() for part in slug.split("-"))[:100]


async def _sync_categories_from_products(db: AsyncSession) -> None:
    product_rows = await db.execute(
        select(Product.category).where(Product.is_active.is_(True), Product.category.is_not(None))
    )
    product_categories = [str(row[0]).strip() for row in product_rows.all() if row[0] and str(row[0]).strip()]
    if not product_categories:
        return

    existing_rows = await db.execute(select(Category.slug, Category.name))
    existing_slugs = set()
    for slug, name in existing_rows.all():
        normalized = _slugify(slug) or _slugify(name)
        if normalized:
            existing_slugs.add(normalized)

    to_add = []
    for raw_category in sorted(set(product_categories)):
        slug = _slugify(raw_category)
        if not slug or slug in existing_slugs:
            continue
        to_add.append(
            Category(
                name=_name_from_slug(slug),
                slug=slug,
                is_active=True,
                description=None,
            )
        )
        existing_slugs.add(slug)

    if to_add:
        db.add_all(to_add)
        await db.commit()


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
    await _sync_categories_from_products(db)

    categories_result = await db.execute(
        select(Category)
        .where(Category.is_active.is_(True))
        .order_by(Category.display_order, Category.name)
    )
    categories = categories_result.scalars().all()
    if not categories:
        return []

    product_rows = await db.execute(
        select(Product.category).where(Product.is_active.is_(True), Product.category.is_not(None))
    )
    product_slugs = {_slugify(str(row[0])) for row in product_rows.all() if row[0]}

    filtered = [
        category
        for category in categories
        if _slugify(category.slug) in product_slugs or _slugify(category.name) in product_slugs
    ]
    if not filtered:
        filtered = categories

    return filtered[skip : skip + limit]


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

    target_slugs = {_slugify(category.slug), _slugify(category.name)}
    target_slugs = {slug for slug in target_slugs if slug}

    result = await db.execute(
        select(Product)
        .where(
            Product.is_active.is_(True),
            Product.category.is_not(None),
        )
        .order_by(Product.created_at.desc())
    )
    products = result.scalars().all()
    filtered = [product for product in products if _slugify(product.category) in target_slugs]
    return filtered[skip : skip + limit]
