from fastapi import APIRouter, HTTPException
from app.schemas.user import Task
from uuid import uuid4
from uuid import UUID
from app.middlewares.response import response

router = APIRouter()

tasks = []  # In-memory database (data is lost when server restarts)

@router.post("/tasks/")
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return response(True, "Task created successfully", task)

@router.get("/tasks/")
def read_tasks():
    return response(True, "Tasks retrieved successfully", tasks)

@router.get("/tasks/{task_id}")
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return response(True, "Task retrieved successfully", task)
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}")
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return response(True, "Task updated successfully", updated_task)
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(idx)
            return response(True, "Task deleted successfully", deleted_task)
    raise HTTPException(status_code=404, detail="Task not found")
