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

# --- Get UserService ---
async def get_user_service(
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(model=Task, session=session)
    return UserService(repository=repo)

#  --- Get TodoService --- 
async def get_todo_service(
    session: AsyncSession = Depends(get_session)
):
    repo = TaskRepository(model=Task, session=session)
    return TaskService(repository=repo)

#  --- Get Current Token --- 
aouthBearerSchema = OAuth2PasswordBearer(tokenUrl="api/token")
async def get_user_token(
    token: str = Depends(aouthBearerSchema)
) -> TokenData:
    payload = decode_jwt(token=token)
    return TokenData(**payload)