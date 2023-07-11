from datetime import date
from pydantic import BaseModel as Base
from pydantic import EmailStr
from pydantic import PositiveInt
from pydantic import validator

class BaseModel(Base):
    class Config:
        orm_mode = True
        use_enum_values = True


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    date_of_birth: date

