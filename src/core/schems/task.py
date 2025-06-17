from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    status: str = Field("todo", pattern="^(todo|in_progress|completed)$")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(todo|in_progress|completed)$")


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True