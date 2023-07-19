import uuid
from datetime import date
from typing import List

from pydantic import BaseModel as Base
from pydantic import EmailStr


class BaseModel(Base):
    class Config:
        orm_mode = True
        use_enum_values = True


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    date_of_birth: date

class BookOutputSchema(BaseModel):
    id: uuid.UUID
    name: str

class UserUpdateSchema(UserCreateSchema):
    pass


class UserOutputSchema(UserCreateSchema):
    id: uuid.UUID
    created_at: date
    updated_at: date
    books: List[BookOutputSchema]
