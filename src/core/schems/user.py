from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from core.schems.task import TaskResponse


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    tasks: List[TaskResponse] = []  
    
    class Config:
        from_attributes = True