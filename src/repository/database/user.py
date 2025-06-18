from sqlalchemy import select

from repository.database.base import BaseRepository
from core.models.user import User
from core.schems.user import UserCreate, UserBase, UserResponse, UserUpdate

class UserRepository(BaseRepository[User]):
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        db_user = User(**user.dict())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return UserResponse.from_orm(db_user)
    
    async def get_user(self , user: UserBase) -> UserResponse:
        pass