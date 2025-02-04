from fastapi import APIRouter, HTTPException, Depends
#from app.schemas.user import Task
from app.models.task import Task  # Using sqlalchemy models for db operations
from sqlalchemy.orm import Session
from app.schemas.task import TaskSchema  # Use TaskSchema from schema/user.py for pydantic validations.
from app.dao.task import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from app.config import get_db

from uuid import uuid4, UUID
from app.middlewares.response import response


router = APIRouter()


# Create a new task
@router.post("/tasks/")
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    task_data = Task(**task.model_dump(exclude={"task_id"}), task_id=uuid4())  # task is automatically validated by Pydantic. ** unpacks py dictionary & passes its keys as arguments (like json o/p).
    created_task = create_task(db, task_data)
    return response(True, "Task created successfully", created_task)


# Get all tasks
@router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_all_tasks(db)
    return response(True, "Tasks retrieved successfully", tasks)


# Get a specific task by task_ID
@router.get("/tasks/{task_id}")
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return response(True, "Task retrieved successfully", task)


# Update a specific task by task_ID
@router.put("/tasks/{task_id}")
def update_task(task_id: UUID, task_update: TaskSchema, db: Session = Depends(get_db)):
    updated_task = update_task(db, task_id, task_update.dict(exclude_unset=True))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return response(True, "Task updated successfully", updated_task)


# Delete a specific task by task_ID
@router.delete("/tasks/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    if not delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return response(True, "Task deleted successfully")

