from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    tag: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())