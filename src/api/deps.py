from fastapi import Depends
from repository.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from core.models.task import Task
from repository.database.user import UserRepository
from repository.database.task import TaskRepository
from core.service.user import UserService
from core.service.task import TaskService

async def get_user_service(
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session, User)
    return UserService(repo)

async def get_todo_service(
    session: AsyncSession = Depends(get_session)
):
    repo = TaskRepository(session, Task)
    return TaskService(repository=repo)