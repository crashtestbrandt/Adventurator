# migrations/env.py

import sys
import pathlib
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
import os

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from Adventorator.db import Base, _normalize_url
from Adventorator import models  # noqa: F401

config = context.config
fileConfig(config.config_file_name)

def get_url():
    url = os.environ.get("DATABASE_URL", "sqlite:///./adventorator.sqlite3")
    return _normalize_url(url)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        from sqlalchemy import create_engine
        connectable = create_engine(get_url().replace("+asyncpg",""))
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
