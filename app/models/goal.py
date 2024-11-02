from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from constants import ID, TITLE

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[list['Task']] = relationship(back_populates='goal')

    def to_dict(self):
        return {
            ID: self.id, 
            TITLE: self.title
        }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data[TITLE])