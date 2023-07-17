import uuid

from fastapi import APIRouter, Depends

from api.v1.user.schema import UserCreateSchema, UserOutputSchema
from core.resolver import get_user_dao_postgres
from dao.postgres.user import UserDatabaseService

router = APIRouter(prefix="/users", tags=["/users"])


@router.post("/")
async def create_user(
    user_schema: UserCreateSchema,
    service: UserDatabaseService = Depends(get_user_dao_postgres),
):
    return await service.create(data=user_schema)


@router.get("/")
async def get_users(service: UserDatabaseService = Depends(get_user_dao_postgres)):
    return await service.get_all()

@router.post('/users/qq')
async def blal(data: UserCreateSchema):
    return data

@router.get("/{user_id}")
async def get_by_id(
    user_id: uuid.UUID, service: UserDatabaseService = Depends(get_user_dao_postgres)
):
    return await service.get(object_id=user_id)


@router.delete("/{user_id}")
async def delete_by_id(
    user_id: uuid.UUID, service: UserDatabaseService = Depends(get_user_dao_postgres)
):
    return await service.delete(object_id=user_id)
