from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db
from constants import ID, TITLE, DESCRIPTION, IS_COMPLETE, COMPLETED_AT, GOAL_ID

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey('goal.id'))
    goal: Mapped[Optional['Goal']] = relationship(back_populates='tasks')

    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        task_dict = {
            ID: self.id, 
            TITLE: self.title,
            DESCRIPTION: self.description,
            IS_COMPLETE: self.is_complete()
        }

        if self.goal_id:
            task_dict[GOAL_ID] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data[TITLE],
            description=task_data[DESCRIPTION],
            completed_at=task_data.get(COMPLETED_AT),
            goal_id=task_data.get(GOAL_ID)
        )