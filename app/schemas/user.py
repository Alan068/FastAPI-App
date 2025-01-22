from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
