import asyncio
from logging.config import fileConfig

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context

# Assuming your application configuration is accessible as shown
from src.conf.config import config as app_config
from src.entity.models import Base

# Alembic Config object, provides access to the values within the .ini file in use.
alembic_config = context.config

# Python logging configuration.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Dynamically setting the SQLAlchemy URL from your application configuration.
alembic_config.set_main_option("sqlalchemy.url", app_config.DB_URL)

# The target metadata for 'autogenerate' support.
target_metadata = Base.metadata

# Run migrations in 'offline' mode.
def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Run migrations in 'online' mode with an asynchronous database connection.
async def run_async_migrations():
    connectable = async_engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations_online_sync)

# Synchronous bridge function for running migrations online with async engine.
def run_migrations_online_sync(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

# Main entry point for running migrations online.
def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

# Determine whether to run in 'offline' mode or 'online' mode based on Alembic context.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()