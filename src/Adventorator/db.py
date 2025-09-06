# db.py

from __future__ import annotations
import contextlib
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from Adventorator.config import load_settings

settings = load_settings()

def _normalize_url(url: str) -> str:
    # Swap sync postgres to async if needed
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

DATABASE_URL = _normalize_url(settings.database_url)

class Base(DeclarativeBase):
    pass

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None

def get_engine() -> AsyncEngine:
    global _engine, _sessionmaker
    if _engine is None:
        _engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)
        _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine

def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if _sessionmaker is None:
        get_engine()
    return _sessionmaker  # type: ignore[return-value]

@contextlib.asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    sm = get_sessionmaker()
    async with sm() as s:
        try:
            yield s
            await s.commit()
        except:  # noqa: E722
            await s.rollback()
            raise
