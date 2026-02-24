from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Async engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        "ssl":"require"
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
