from typing import TypeVar
from pydantic import BaseModel

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from src.core.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL)

DatabaseModel = TypeVar("DatabaseModel", bound=DeclarativeBase)
Schema = TypeVar("Schema", bound=BaseModel)


def get_async_session() -> async_sessionmaker:
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
