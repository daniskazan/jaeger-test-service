from api.v1.user.schema import UserSchema
from dao.base import DatabaseService
from models.user import User


class UserDatabaseService(DatabaseService[User, UserSchema]):
    pass



