from core.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")  # "admin" или "user"
    created_at = Column(Integer, default=datetime.now(timezone.utc))

    tasks = relationship("Task", back_populates="owner")