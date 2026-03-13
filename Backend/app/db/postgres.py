from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.db.base import Base
from app.models.user_model import User, UserRole
from app.utils.hashing import get_password_hashed

# Async engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT_SECONDS,
    connect_args={
        # "ssl":"require",
        "ssl":False,
        "command_timeout": 30,
    }
)


AsyncSessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession, autoflush=False, autocommit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Dependency
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_default_admin()


async def seed_default_admin():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        existing = result.scalars().first()
        if existing:
            if existing.role != UserRole.admin:
                existing.role = UserRole.admin
                await session.commit()
            return

        admin = User(
            name=settings.ADMIN_NAME,
            email=settings.ADMIN_EMAIL,
            password=get_password_hashed(settings.ADMIN_PASSWORD),
            role=UserRole.admin,
            is_blocked=False,
        )
        session.add(admin)
        await session.commit()
