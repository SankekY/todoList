from core.models.base import Base
from sqlalchemy import Integer, String, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    status = Column(String(20))  # "todo", "in_progress", "completed"
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")