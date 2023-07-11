import punq
from aiokafka import AIOKafkaProducer
from aiocache import RedisCache
from loguru import logger

from api.v1.user.schema import UserSchema
from core.settings import settings
from core import redis
from core import kafka
from dao.base import DatabaseService
from dao.postgres.user import UserDatabaseService
from models.user import User

container = punq.Container()


async def register_deps() -> None:

    kafka.aioproducer = AIOKafkaProducer(  # noqa
        client_id='authorization-service',
        acks='all',
        enable_idempotence=True,
        bootstrap_servers=settings.KAFKA_DSN
    )
    redis.cache = RedisCache(endpoint=settings.REDIS_HOST, port=settings.REDIS_PORT)
    user_service = UserDatabaseService(model=User, schema=UserSchema)

    container.register(service=AIOKafkaProducer, instance=kafka.aioproducer)

    container.register(service=RedisCache, instance=redis.cache)
    container.register(UserDatabaseService, instance=user_service)



    kafka_producer = container.resolve(service_key=AIOKafkaProducer)
    await kafka_producer.start()
    logger.info("All services initialized")


async def stop_services() -> None:
    await container.resolve(service_key=AIOKafkaProducer).stop()
    await container.resolve(service_key=RedisCache).close()


def get_redis_client() -> RedisCache:
    return container.resolve(service_key=RedisCache)


def get_kafka_producer():
    return container.resolve(service_key=AIOKafkaProducer)

def get_user_dao_postgres() -> UserDatabaseService:
    return container.resolve(service_key=UserDatabaseService)
