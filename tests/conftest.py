# tests/conftest.py

import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from Adventorator.db import Base
from typing import AsyncIterator  # <-- add this (or from collections.abc)

@pytest.fixture(scope="session")
async def test_sessionmaker() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./adventurator_test.sqlite3"
    engine = create_async_engine(os.environ["DATABASE_URL"], future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()

@pytest.fixture
async def db(test_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    async with test_sessionmaker() as s:
        try:
            yield s
        finally:
            await s.rollback()
