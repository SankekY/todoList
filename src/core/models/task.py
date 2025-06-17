from core.models.base import Base
from sqlalchemy import Integer, String, Column

class Task(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    status = Column(String(20))  # "todo", "in_progress", "completed"
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")