from typing import Optional
from pydantic import BaseModel, Field, EmailStr
import uuid

from core.settings import settings


class UserCreateSchema(BaseModel):
    user_id: uuid.UUID = Field(default_factory=str(uuid.uuid4))
    name: str
    email: EmailStr
    age: int = Field(default=20, gt=0, lt=100)

    class Kafka:
        topic = f"{settings.KAFKA_TOPIC_PREFIX}.event.user-registered"
