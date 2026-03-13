from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banner_model import Banner


async def list_active_banners(db: AsyncSession) -> list[Banner]:
    result = await db.execute(
        select(Banner).where(Banner.is_active.is_(True)).order_by(Banner.display_order.asc(), Banner.id.asc())
    )
    return result.scalars().all()


async def list_all_banners(db: AsyncSession) -> list[Banner]:
    result = await db.execute(select(Banner).order_by(Banner.display_order.asc(), Banner.id.asc()))
    return result.scalars().all()


async def create_banner(db: AsyncSession, data: dict) -> Banner:
    banner = Banner(**data)
    db.add(banner)
    await db.commit()
    await db.refresh(banner)
    return banner


async def update_banner(db: AsyncSession, banner_id: int, data: dict) -> Banner | None:
    banner = await db.get(Banner, banner_id)
    if not banner:
        return None
    for key, value in data.items():
        setattr(banner, key, value)
    await db.commit()
    await db.refresh(banner)
    return banner


async def delete_banner(db: AsyncSession, banner_id: int) -> bool:
    banner = await db.get(Banner, banner_id)
    if not banner:
        return False
    await db.delete(banner)
    await db.commit()
    return True
