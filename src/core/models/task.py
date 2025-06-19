from core.models.base import Base
from sqlalchemy import Integer, String, Column, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import timezone, datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    status = Column(String(20))  # "todo", "in_progress", "completed"
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    created_at = Column(DateTime, default=datetime.now(timezone.utc))