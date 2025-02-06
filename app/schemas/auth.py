from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID


class UserCreate(BaseModel):   # Validates input during user registration.
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):   # For returning user details during authentication.
    user_id: UUID
    username: str
    email: EmailStr
    role: str


    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)  # Pydantic v2 replacement for orm_mode, Allows UUID in the schema.

    # class Config:
    #     orm_mode = True

class Token(BaseModel):   # Represents the JWT token returned after successful login.
    access_token: str
    token_type: str

class TokenData(BaseModel):   # Decoded data. Used internally to validate and extract data from JWT tokens during authentication.
    username: Optional[str] = None   # Optional as token might now contain valid user info.