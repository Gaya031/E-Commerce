import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from app.db.base import Base
from app.core.config import settings

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models so Alembic can detect them
import app.models.user_model
import app.models.seller_model
import app.models.product_model
import app.models.order_model
import app.models.payment_model
import app.models.delivery_model
import app.models.subscription_model
import app.models.review_model
import app.models.commission_model

target_metadata = Base.metadata


def get_database_url() -> str:
    return settings.DATABASE_URL


# -------------------------
# OFFLINE MIGRATIONS
# -------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# # -------------------------
# # ONLINE MIGRATIONS (ASYNC)
# # -------------------------
# async def run_migrations_online() -> None:
#     configuration = config.get_section(config.config_ini_section)
#     configuration["sqlalchemy.url"] = get_database_url()

#     engine = async_engine_from_config(
#         configuration,
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     async with engine.connect() as connection:
#         await connection.run_sync(
#             lambda sync_conn: context.configure(
#                 connection=sync_conn,
#                 target_metadata=target_metadata,
#                 compare_type=True,
#                 compare_server_default=True,
#             )
#         )

#         await connection.run_sync(context.run_migrations)

#     await engine.dispose()


# -------------------------
# ONLINE MIGRATIONS (ASYNC)
# -------------------------
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    engine = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()



# -------------------------
# ENTRY POINT
# -------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
