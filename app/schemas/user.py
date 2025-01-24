from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional

class TaskSchema(BaseModel):
    task_id: Optional[str] = None
    task_name: str = Field(..., max_length=50)
    task_description: Optional[str] = None
    assignee: str = Field(..., max_length=50)
    assignor: str = Field(..., max_length=50)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    task_deadline: Optional[date] = None
    completed: bool = False

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models


