from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from ..db import db
from constants import ID, TITLE, DESCRIPTION, IS_COMPLETE

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=None)

    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        return {
            ID: self.id, 
            TITLE: self.title,
            DESCRIPTION: self.description,
            IS_COMPLETE: self.is_complete()
        }