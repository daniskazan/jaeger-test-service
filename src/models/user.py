from datetime import datetime
from sqlalchemy.sql.sqltypes import String, DateTime, Boolean

from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class User(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, index=True
    )
    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<User> {self.username}"
