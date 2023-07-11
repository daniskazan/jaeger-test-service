from typing import (
    Generic,
    Type
)
from sqlalchemy import insert

from dao import DatabaseModel, Schema, get_async_session


class DatabaseService(Generic[DatabaseModel, Schema]):
    session = get_async_session()

    def __init__(self, model: Type[DatabaseModel], schema: Type[Schema]):
        self.model = model
        self.schema = schema

    async def get(self): pass

    async def create(self, data: Schema):
        async with self.session() as session:
            query = insert(self.model).values(data.dict())
            created_model = await session.execute(statement=query)
            await session.commit()
        return created_model

    async def update(self): pass

    async def delete(self): pass



