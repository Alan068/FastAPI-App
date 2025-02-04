from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config import Base
import enum
from sqlalchemy.orm import DeclarativeBase
from .base import Base  # Importing Base for db migrations


class UserRole(enum.Enum):
    user = "user"
    manager = "manager"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4, unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False)  # User, Manager, Admin
