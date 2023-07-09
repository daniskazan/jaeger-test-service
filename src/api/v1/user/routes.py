import uuid

from fastapi import APIRouter, Depends
from aiocache import RedisCache

from core.resolver import get_redis_client, get_user_dao_redis
from dao.redis.user import UserDaoRedis
from models.user import UserCreateSchema

router = APIRouter(prefix='/users', tags=["/users"])



@router.post('/')
async def create_user(data: UserCreateSchema, user_dao: UserDaoRedis = Depends(get_user_dao_redis)):
    return await user_dao.create_user(data)


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, user_dao: UserDaoRedis = Depends(get_user_dao_redis)):
    print(user_dao.kafka)
    return await user_dao.get_user(user_id=user_id)


@router.delete("/{user_id}")
async def delete_user(user_id: uuid.UUID, user_dao: UserDaoRedis = Depends(get_user_dao_redis)):
    return await user_dao.delete(user_id=user_id)


@router.get("/")
async def get_all_users(user_dao: UserDaoRedis = Depends(get_user_dao_redis)):
    return await user_dao.get_all()