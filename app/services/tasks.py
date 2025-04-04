from sqlalchemy.orm import Session
from datetime import datetime, date
from app.models.task import Task
from app.schemas.task import TaskCreate


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()


def get_tasks_by_day(db: Session, day: date, user_id: int):
    return (
        db.query(Task)
        .filter(
            Task.start_date_time >= datetime.combine(day, datetime.min.time()),
            Task.start_date_time <= datetime.combine(day, datetime.max.time()),
            Task.owner_id == user_id,
        )
        .all()
    )


def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(
        status=task.status,
        card_title=task.card_title,
        tag_title=task.tag.title,
        tag_color=task.tag.color,
        start_date_time=task.start_date_time,
        end_date_time=task.end_date_time,
        owner_id=user_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskCreate, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db_task.status = task.status
        db_task.card_title = task.card_title
        db_task.tag_title = task.tag.title
        db_task.tag_color = task.tag.color
        db_task.start_date_time = task.start_date_time
        db_task.end_date_time = task.end_date_time
        db.commit()
        db.refresh(db_task)
    return db_task
