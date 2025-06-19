from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = None
    status: str = Field("todo", pattern="^(todo|in_progress|completed)$")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(None, max_length=100)
    description: str | None = None
    status: str | None = Field(None, pattern="^(todo|in_progress|completed)$")


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True