from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Async engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT_SECONDS,
    connect_args={
        "ssl":"require",
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
