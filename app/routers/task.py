from fastapi import APIRouter, HTTPException, Depends
#from app.schemas.user import Task
from app.models.task import Task  # Using sqlalchemy models for db operations
from sqlalchemy.orm import Session
from app.schemas.task import TaskSchema  # Use TaskSchema from schema/user.py for pydantic validations.
from app.config import get_db

from uuid import uuid4, UUID
from app.middlewares.response import response


router = APIRouter()


# Create a new task
@router.post("/tasks/")
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    db_task = Task(**task.model_dump(exclude={"task_id"}), task_id=uuid4())  # task is automatically validated by Pydantic. ** unpacks py dictionary & passes its keys as arguments (like json o/p).
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return response(True, "Task created successfully", db_task)


# Read all Tasks
@router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return response(True, "Tasks retrieved successfully", tasks)


# Read a specific Task by task_id
@router.get("/tasks/{task_id}")
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return response(True, "Task retrieved successfully", task)


# Update a specific Task by task_id
@router.put("/tasks/{task_id}")
def update_task(task_id: UUID, task_update: TaskSchema, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return response(True, "Task updated successfully", db_task)


# Delete a specific Task by task_id
@router.delete("/tasks/{task_id}")
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return response(True, "Task deleted successfully", db_task)
