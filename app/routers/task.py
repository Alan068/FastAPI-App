from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4, UUID

from app.models.user import User
from app.schemas.task import TaskSchema  # For Pydantic validations
from app.dao.task import (
    dao_create_task, get_all_tasks, get_task_by_id,
    dao_update_task, dao_delete_task, dao_review_task
)

from app.config import get_db
from app.middlewares.response import response
from app.middlewares.auth import get_current_user, manager_required

router = APIRouter()



# Create a new task (Only managers)
@router.post("/tasks/", dependencies=[Depends(manager_required)])
def create_task(task: TaskSchema, db: Session = Depends(get_db), current_user: User = Depends(manager_required)):
    task_data = task.model_dump(exclude={"task_id", "assignor"})

    task_data["task_id"] = str(uuid4())  # Generate new task ID
    task_data["assignor"] = str(current_user.user_id)  # Getting assignor value from token

    created_task = dao_create_task(db, task_data, current_user)
    return response(True, "Task created successfully", created_task)



# Get all tasks (Users see only their tasks, managers/admins see all)
@router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = get_all_tasks(db, current_user)
    return response(True, "Tasks retrieved successfully", tasks)



# Get a specific task by task_ID (Only assigned users or managers)
@router.get("/tasks/{task_id}")
def read_task(task_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    task = get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return response(True, "Task retrieved successfully", task)



# Update a task (Only managers or assigned users)
@router.put("/tasks/{task_id}")
def update_task(task_id: UUID, task_update: TaskSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    updated_task = dao_update_task(db, task_id, task_update.model_dump(exclude_unset=True), current_user)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return response(True, "Task updated successfully", updated_task)



# Delete a task (Only managers/admins)
@router.delete("/tasks/{task_id}", dependencies=[Depends(manager_required)])
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    if not dao_delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return response(True, "Task deleted successfully")



# Manager review and update task status
@router.put("/tasks/{task_id}/review", dependencies=[Depends(manager_required)])
def review_task(task_id: UUID, task_update: TaskSchema, db: Session = Depends(get_db), current_user: User = Depends(manager_required)):

    reviewed_task = dao_review_task(db, task_id, task_update.model_dump(exclude_unset=True), current_user)
    if not reviewed_task:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    return response(True, "Task reviewed successfully", reviewed_task)
