from datetime import datetime
import uuid

from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.utc_timestamp()
    )
