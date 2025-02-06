from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class UserUpdate(BaseModel):  # For updating user details
    user_id: UUID
    username: Optional[str]
    email: Optional[str]

class UserDetail(BaseModel):  # For viewing user details
    user_id: UUID
    username: str
    email: str
    role: str  # "user", "manager", or "admin"

    class Config:
        orm_mode = True
