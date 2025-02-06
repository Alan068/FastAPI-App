from sqlalchemy.orm import Session
from app.models.task import Task
from uuid import UUID


def create_task(db: Session, task_data: dict) -> Task:
    task = Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: UUID) -> Task | None:
    return db.query(Task).filter(Task.task_id == task_id).first()

def update_task(db: Session, task_id: UUID, task_data: dict) -> Task | None:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        return None
    for key, value in task_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: UUID) -> bool:
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
