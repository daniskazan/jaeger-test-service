from typing import TypeVar
from pydantic import BaseModel

from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL)

DatabaseModel = TypeVar("DatabaseModel", bound=DeclarativeBase)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


def get_async_session() -> Session:
    session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session()
