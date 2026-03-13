from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from app.core.config import settings
from app.db.base import Base
import app.models  # noqa: F401 - ensures model metadata is registered before create_all
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
        await migrate_geo_columns(conn)
    await seed_default_admin()


async def migrate_geo_columns(conn) -> None:
    columns = [
        ("users", "latitude"),
        ("users", "longitude"),
        ("sellers", "latitude"),
        ("sellers", "longitude"),
    ]
    for table_name, column_name in columns:
        result = await conn.execute(
            text(
                """
                SELECT data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = :table_name
                  AND column_name = :column_name
                """
            ),
            {"table_name": table_name, "column_name": column_name},
        )
        data_type = result.scalar()
        if data_type not in {"character varying", "text"}:
            continue
        await conn.execute(
            text(
                f"""
                ALTER TABLE {table_name}
                ALTER COLUMN {column_name} TYPE DOUBLE PRECISION
                USING (
                  CASE
                    WHEN {column_name} IS NULL THEN NULL
                    WHEN trim({column_name}::text) = '' THEN NULL
                    WHEN trim({column_name}::text) ~ '^-?[0-9]+(\\.[0-9]+)?$'
                      THEN trim({column_name}::text)::double precision
                    ELSE NULL
                  END
                )
                """
            )
        )


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
