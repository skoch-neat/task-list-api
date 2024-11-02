from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db
from constants import ID, TITLE, DESCRIPTION, IS_COMPLETE, COMPLETED_AT

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey('goal.id'))
    goal: Mapped[Optional['Goal']] = relationship(back_populates='tasks')

    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        return {
            ID: self.id, 
            TITLE: self.title,
            DESCRIPTION: self.description,
            IS_COMPLETE: self.is_complete()
        }
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data[TITLE],
            description=task_data[DESCRIPTION],
            completed_at=task_data.get(COMPLETED_AT)
        )     