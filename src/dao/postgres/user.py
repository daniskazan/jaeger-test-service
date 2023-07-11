from api.v1.user.schema import UserCreateSchema, UserOutputSchema, UserUpdateSchema
from dao.base import DatabaseService
from models.user import User


class UserDatabaseService(
    DatabaseService[User, UserCreateSchema, UserUpdateSchema, UserOutputSchema]
):
    pass
