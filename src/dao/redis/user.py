import uuid

from aiocache import RedisCache
from aiokafka import AIOKafkaProducer
from fastapi import HTTPException, Response, status
from models.user import User
from api.v1.user.schema import UserSchema


# class UserDaoRedis:
#     def __init__(self, client: RedisCache, kafka: AIOKafkaProducer):
#         self.client = client
#         self.kafka = kafka
#
#     async def get_user(self, user_id: uuid.UUID):
#         user = await self.client.get(f"user:info:{user_id}")
#         if user:
#             return UserSchema.parse_raw(user)
#         raise HTTPException(status_code=404, detail=f"User #{user_id} not found")
#
#     async def create_user(self, data: UserSchema):
#
#         if exists := await self.client.get(f"user:info:{data.}"):
#             raise HTTPException(status_code=400, detail=f"fUser #{data.user_id} exists")
#         await self.client.set(f"user:info:{data.user_id}", data.json())
#         return Response(status_code=status.HTTP_201_CREATED, content='null')
#
#         await self.kafka.send(topic=data.Kafka.topic, value=data.json().encode(), key=str(data.user_id).encode())
#
#     async def delete(self, user_id: uuid.UUID):
#         await self.client.delete(key=f"user:info:{user_id}")
#         return None
#
#     async def get_all(self):
#         return await self.client.multi_get(keys=["user:info:"])
