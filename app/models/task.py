from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from constants import ID, TITLE, DESCRIPTION, IS_COMPLETE

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    is_complete: Mapped[datetime] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            ID: self.id, 
            TITLE: self.title,
            DESCRIPTION: self.description,
            IS_COMPLETE: self.is_complete
        }