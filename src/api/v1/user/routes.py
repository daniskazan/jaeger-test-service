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
