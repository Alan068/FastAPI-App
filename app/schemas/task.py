from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional



class TaskSchema(BaseModel):

    task_name: str = Field(..., max_length=50)
    task_description: str = None

    assignee: str                                # assignee: str = Field(..., max_length=50)
    # assignor: str                              No need in req body, getting through token  # assignor: str = Field(..., max_length=50)

    start_date: date = None  # Provided by the assignor not user/assignee
    end_date: date = None  # Provided by the assignor not user/assignee
    task_deadline: date
    status: Optional[str] = Field(default="pending")
    feedback: Optional[str] = Field(default="")



    # completed: bool = False

    # class Config:
    #     orm_mode = True  # Allows Pydantic to work with SQLAlchemy models


