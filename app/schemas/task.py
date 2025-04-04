from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class EventCardStatus(str, Enum):
    canceled = "canceled"
    done = "done"
    backlog = "backlog"


class Tag(BaseModel):
    title: str
    color: str


class TaskBase(BaseModel):
    status: EventCardStatus = EventCardStatus.backlog
    card_title: str
    tag: Tag
    start_date_time: datetime
    end_date_time: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
