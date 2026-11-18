"""ORM model for the introductory Test table."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TestRecord(Base):
    """A simple record used to demonstrate database persistence."""

    __tablename__ = "Test"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    date_inserted: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
