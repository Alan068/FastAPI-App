from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config import Base


class Task(Base):
    __tablename__ = "tasks"


    # task_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)

    task_id = Column(UUID, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    task_name = Column(String(50), unique=True, nullable=False)
    task_description = Column(Text, nullable=False)
    assignee = Column(String(50), nullable=False)
    assignor = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    task_deadline = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
