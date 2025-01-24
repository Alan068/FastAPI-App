from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.config import Base


class Task(Base):
    __tablename__ = "tasks"


    task_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    task_name = Column(String(50), unique=True, nullable=False)
    task_description = Column(Text, nullable=True)
    assignee = Column(String(50), nullable=False)
    assignor = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    task_deadline = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
