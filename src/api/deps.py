from fastapi import Depends
from repository.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

# --- Authorize import --- 
from fastapi.security import OAuth2PasswordBearer
from core.schems.token import Token, TokenData
from utils.auth_jwt import decode_jwt

# --- User import --- 
from repository.database.user import UserRepository
from core.service.user import UserService
from core.models.user import User

# --- Tasks import --- 
from repository.database.task import TaskRepository
from core.service.task import TaskService
from core.models.task import Task

# --- Depends Code ---
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

aouthBearerSchema = OAuth2PasswordBearer(tokenUrl="api/auth/token")
async def get_user_token(
    token: aouthBearerSchema = Depends()
) -> TokenData:
    payload = decode_jwt(token=token)
    return TokenData(**payload)