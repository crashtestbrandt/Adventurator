# migrations/env.py

import sys
import pathlib
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from Adventorator.db import Base, _normalize_url
import os
import sys

from Adventorator.db import Base, _normalize_url

config = context.config
fileConfig(config.config_file_name)

def get_url():
    url = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./adventorator.sqlite3")
    # For Alembic's sync engine, drop the '+driver' part
    return url.replace("+asyncpg", "").replace("+aiosqlite", "")

target_metadata = Base.metadata

def get_url() -> str:
    url = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./adventorator.sqlite3")
    # Alembic uses a sync engine; strip async driver suffixes
    return url.replace("+asyncpg", "").replace("+aiosqlite", "")

def run_migrations_offline():
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Create a sync engine
    from sqlalchemy import create_engine
    connectable = create_engine(get_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()