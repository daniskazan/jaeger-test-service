from typing import List
from sqlalchemy.sql.sqltypes import String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .association_table import user_book_mapping


class Book(Base):
    __tablename__ = "books"
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    authors: Mapped[List["User"]] = relationship(
        secondary=user_book_mapping, back_populates="books"
    )
