from sqlalchemy import (
    Column,
    Table,
    ForeignKey
)

from models.base import Base

user_book_mapping = Table(
    "user_book",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)