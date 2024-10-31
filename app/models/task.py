from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from constants import ID, NAME, DESCRIPTION, COMPLETED_AT

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            ID: self.id, 
            NAME: self.name,
            DESCRIPTION: self.description,
            COMPLETED_AT: self.completed_at
        }