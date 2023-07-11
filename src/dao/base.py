from typing import Generic, Type
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from dao import (
    DatabaseModel,
    UpdateSchema,
    CreateSchema,
    OutputSchema,
    get_async_session,
)


class DatabaseService(Generic[DatabaseModel, CreateSchema, UpdateSchema, OutputSchema]):
    def __init__(
        self,
        model: Type[DatabaseModel],
        create_schema: Type[CreateSchema],
        update_schema: Type[UpdateSchema],
        output_schema: Type[OutputSchema],
    ):
        self.session = get_async_session()
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.output_schema = output_schema

    async def get(self):
        pass

    async def create(self, data: CreateSchema):
        async with self.session() as session:
            query = insert(self.model).values(data.dict())
            created_model = await session.execute(statement=query)
            await session.commit()
        return created_model.scalar_one()

    async def update(self):
        pass

    async def delete(self):
        pass

    async def get_all(self):
        async with self.session() as session:
            query = select(self.model)
            response = await session.execute(query)
            rows = response.all()
            return [self.output_schema.from_orm(row._data[0]) for row in rows]
