from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionDep
from datetime import date, datetime
from typing import Optional
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.tasks import get_task, get_tasks_by_day, create_task, update_task
from app.auth.auth import get_current_user

router = APIRouter()


@router.get("/tasks", response_model=list[Task])
def read_tasks(
    session: SessionDep,
    day: Optional[date] = None,
    current_user = Depends(get_current_user),
):
    print('current_user', current_user)
    if day is None:
        day = datetime.now().date()
    tasks = get_tasks_by_day(session, day=day, user_id=current_user.get("id"))
    return [{
        "id": task.id,
        "status": task.status,
        "card_title": task.card_title,
        "tag": { "title": task.tag_title, "color": task.tag_color },
        "start_date_time": task.start_date_time,
        "end_date_time": task.end_date_time,
        "owner_id": task.owner_id
    } for task in tasks]


@router.post("/tasks", response_model=Task)
def create_new_task(
    task: TaskCreate,
    session: SessionDep,
    current_user = Depends(get_current_user),
):
    created_task = create_task(db=session, task=task, user_id=current_user.get("id"))
    return {
        "id": created_task.id,
        "status": created_task.status,
        "card_title": created_task.card_title,
        "tag": { "title": created_task.tag_title, "color": created_task.tag_color },
        "start_date_time": created_task.start_date_time,
        "end_date_time": created_task.end_date_time,
        "owner_id": created_task.owner_id
    }


@router.get("/tasks/{task_id}/info", response_model=Task)
def read_task(
    task_id: int,
    session: SessionDep,
    current_user = Depends(get_current_user),
):
    db_task = get_task(session, task_id=task_id, user_id=current_user.get("id"))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": db_task.id,
        "status": db_task.status,
        "card_title": db_task.card_title,
        "tag": { "title": db_task.tag_title, "color": db_task.tag_color },
        "start_date_time": db_task.start_date_time,
        "end_date_time": db_task.end_date_time,
        "owner_id": db_task.owner_id
    }


@router.put("/tasks/{task_id}/edit", response_model=Task)
def update_task_details(
    task_id: int,
    task: TaskUpdate,
    session: SessionDep,
    current_user = Depends(get_current_user),
):
    db_task = get_task(session, task_id=task_id, user_id=current_user.get("id"))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = update_task(db=session, task_id=task_id, task=task, user_id=current_user.get("id"))
    return {
        "id": updated_task.id,
        "status": updated_task.status,
        "card_title": updated_task.card_title,
        "tag": { "title": updated_task.tag_title, "color": updated_task.tag_color },
        "start_date_time": updated_task.start_date_time,
        "end_date_time": updated_task.end_date_time,
        "owner_id": updated_task.owner_id
    }
