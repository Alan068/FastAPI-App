from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserResponse
from app.models.user import User
from app.config import get_db
from app.middlewares.auth import get_current_user, get_current_admin
from app.middlewares.response import response
from uuid import UUID

router = APIRouter()

# Get all users (admin-only)
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_user = db.query(User).all()
    return response(True, "Users retrieved successfully", db_user)


# Get the current user's profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return response(True, "Profile retrieved successfully", current_user)


# Update a user's role (admin-only)
@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: UUID, role: str, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if role not in ["user", "manager", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return response(True, f"User role updated to {role}", db_user)


import secrets
import uuid
print(secrets.token_urlsafe(32))  # This will generate a 32-byte URL-safe secret key.
