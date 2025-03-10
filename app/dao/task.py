from sqlalchemy.orm import Session
from app.models.task import Task
from uuid import UUID
from app.schemas.task import TaskSchema
from app.models.user import User
from fastapi import HTTPException


def dao_create_task(db: Session, task_data: dict, current_user: User) -> Task:
    print(f"Assignee ID Type: {type(task_data['assignee'])}, Value: {task_data['assignee']}")
    print(f"Assignor ID Type: {type(current_user.user_id)}, Value: {current_user.user_id}")

    assignee_id = str(task_data["assignee"])  # Converting to str
    assignee = db.query(User).filter(User.user_id == assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="User not found!")

    task_data["assignor"] = str(current_user.user_id)  # Converting to str

    task = Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all_tasks(db: Session, current_user: User) -> list[Task]:
    print(f"User Role: {current_user.role}, User ID: {current_user.user_id}")  # debug
    user_role = current_user.role.value

    if user_role in ["manager", "admin"]:
        tasks = db.query(Task).all()
        print(f"Retrieved {len(tasks)} tasks for admin/manager")                    # debug
        return tasks

    tasks = db.query(Task).filter(Task.assignee == current_user.user_id).all()
    print(f"Retrieved {len(tasks)} tasks for user")                                  # debug
    return tasks



def get_task_by_id(db: Session, task_id: UUID, current_user: User) -> Task | None:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task or (task.assignee != current_user.user_id and current_user.role.value not in ["manager", "admin"]):
        return None
    return task



def dao_update_task(db: Session, task_id: UUID, task_data: dict, current_user: User) -> Task | None:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task or (task.assignee != current_user.user_id and current_user.role.value not in ["manager", "admin"]):
        return None
    for key, value in task_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task



def dao_delete_task(db: Session, task_id: UUID) -> bool:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return True



def dao_review_task(db: Session, task_id: UUID, task_update: TaskSchema, current_user: User):
    if current_user.role.value != "manager":
        raise HTTPException(status_code=403, detail="Only managers can update task status or feedback")

    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        return None

    if task_update.feedback:          # Update feedback and task if provided
        task.feedback = task_update.feedback
    if task_update.status:
        task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task
