from fastapi import Depends
from repository.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from repository.database.user import UserRepository
from core.service.user import UserService

async def get_user_service(
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session, User)
    return UserService(repo)