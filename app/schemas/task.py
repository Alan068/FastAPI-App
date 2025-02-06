from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date


class TaskSchema(BaseModel):
    # task_id: str = None  # Dont need this Since it will be generated from backend instead of being given by user.

    task_name: str = Field(..., max_length=50)
    task_description: str = None
    assignee: str = Field(..., max_length=50)
    assignor: str = Field(..., max_length=50)
    start_date: date = None  # Provided by the assignor not user/assignee
    end_date: date = None  # Provided by the assignor not user/assignee
    task_deadline: date

    # completed: bool = False

    # class Config:
    #     orm_mode = True  # Allows Pydantic to work with SQLAlchemy models


