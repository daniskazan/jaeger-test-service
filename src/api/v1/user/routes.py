import uuid

from fastapi import APIRouter, Depends

from api.v1.user.schema import UserSchema
from core.resolver import get_user_dao_postgres
from dao.postgres.user import UserDatabaseService


router = APIRouter(prefix='/users', tags=["/users"])



@router.post('/')
async def create_user(user_schema: UserSchema, service: UserDatabaseService = Depends(get_user_dao_postgres)):
    return await service.create(data=user_schema)
