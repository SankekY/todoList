from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List, Optional, Any
from core.schems.task import TaskResponse
from core.models.user import User
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None 

    class Config:
        from_attributes = True

    @model_validator(mode='before')
    @classmethod
    def prepare_response(cls, data: Any) -> Any:
        if isinstance(data, User):
            return {
                "id": data.id,
                "email": data.email,
                "username": data.username,
                "is_active": data.is_active,
                "role": data.role,
                "created_at": data.created_at,
                "tasks": []  # Пустой список по умолчанию
            }
        return data

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=30)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UserTokenData(UserBase):
    id: int | None = None
    email: str | None = None
    is_active: bool | None = None
    role: str | None = None

class UserWithTasks(UserBase):
    id: int  # Add this required field
    is_active: bool  # Add other required fields from UserResponse if needed
    role: str
    created_at: datetime
    tasks: List[TaskResponse] = []

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    tasks: List[TaskResponse] = []
    created_at: datetime


