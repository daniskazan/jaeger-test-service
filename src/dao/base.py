from typing import Generic, Type, List, Union
from uuid import UUID

from fastapi import HTTPException

from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy import Select, func, select, or_
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload

from dao import (
    DatabaseModel,
    UpdateSchema,
    CreateSchema,
    OutputSchema,
    get_async_session,
)


class DatabaseService(Generic[DatabaseModel, CreateSchema, UpdateSchema, OutputSchema]):
    class Config:
        instance_verbose_name = "Объект"

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

    async def _get_instance(self, **kwargs) -> DatabaseModel:
        cond = [getattr(self.model, k) == v for k, v in kwargs.items()]
        query = select(self.model).where(*cond).options(selectinload("*"))
        return await self._execute_with_not_found_handler(query, **kwargs)

    async def _execute_with_not_found_handler(
        self, query: Select, **kwargs
    ) -> DatabaseModel:
        response = await self.session.execute(query)
        try:
            instance = response.scalar_one()
        except NoResultFound:
            key, value = kwargs.popitem()
            raise HTTPException(
                status_code=404,
                detail={
                    "system_message": f"{self.Config.instance_verbose_name} с {key}='{value}' не найден."
                },
            )
        return instance

    async def get(self, object_id: UUID) -> OutputSchema:
        instance = await self._get_instance(id=object_id)
        return self.output_schema.from_orm(instance)

    async def delete(self, object_id: UUID):
        instance = await self._get_instance(id=object_id)
        await self.session.delete(instance=instance)
        await self.session.commit()
        return {"deleted": object_id}

    async def create(self, data: CreateSchema) -> OutputSchema:
        instance = self.model(**data.dict())
        self.session.add(instance)
        await self.session.commit()
        return self.output_schema.from_orm(instance)

    async def get_by_ids(
        self,
        list_ids: List[Union[str, UUID]],
    ) -> List[DatabaseModel]:
        query = select(self.model).where(self.model.id.in_(list_ids))
        response = await self.session.execute(query)
        try:
            result: ChunkedIteratorResult = response.all()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Не найдено")
        return [self.output_schema(obj._data[0]) for obj in result]

    async def get_all(self) -> List[OutputSchema]:
        query = select(self.model)
        result: ChunkedIteratorResult = await self.session.execute(query)

        return [self.output_schema.from_orm(obj._data[0]) for obj in result.unique()]
