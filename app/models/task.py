from sqlalchemy import Column, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"


    task_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    task_name = Column(String(50), unique=True, nullable=False)
    task_description = Column(Text, nullable=False)

    assignee = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    assignor = Column(String(36), ForeignKey("users.user_id"), nullable=False)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    task_deadline = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    status = Column(String, default="Pending")  # Added status field which will be updated by manager(pending, finished, reviewed) 14/02/25
    feedback = Column(String, default="", nullable=True)  # Added feedback field 14/02/25


    assignor_user = relationship("User", foreign_keys=[assignor])
    assignee_user = relationship("User", foreign_keys=[assignee])
