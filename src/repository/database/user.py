from sqlalchemy import select

from repository.database.base import BaseRepository
from core.models.user import User
from core.schems.user import UserCreate, UserBase, UserResponse, UserUpdate
from utils.auth_jwt import hash_password
from fastapi import HTTPException

class UserRepository(BaseRepository[User]):
    
    async def create_user(self, user: UserCreate) -> UserResponse:
        """
        Создает нового пользователя в базе данных
        Args:
            user: Данные для создания пользователя (UserCreate schema)
        Returns:
            UserResponse: Созданный пользователь
        Raises:
            HTTPException: При ошибках валидации или существующем пользователе
        """
        try:
            existing_user = await self.session.execute(
                select(User).where(
                    (User.email == user.email) | 
                    (User.username == user.username)
                )
            )
            if existing_user.scalar_one_or_none():
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь с таким email или username уже существует"
                )
            db_user = User(
                username=user.username,
                email=user.email,
                password_hash=hash_password(user.password)
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return UserResponse.model_validate(db_user)
            
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при создании пользователя: {str(e)}"
            )
    
    async def get_user(self, user: UserBase) -> UserResponse | None:
        try:
            existing_user = await self.session.execute(
            select(User).where(
                    (User.username == user.username) |
                    (User.email == user.email)
                )
            )
            return existing_user.scalar_one_or_none()

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при получении пользователя: {str(e)}"
            )

    async def update_user(self, user: UserUpdate, id: int) -> UserResponse | None:
        try:
            existing_user = await self.session.execute(select(User).where(User.id == id))

            user_db = existing_user.scalar_one_or_none()
            if not user_db:
                return None
            
            update_dict = user.model_dump(exclude_unset=True)
            if "password" in update_dict:
                user_db.password_hash = hash_password(update_dict.pop("password"))
            for field, value in update_dict.items():
                setattr(user_db, field, value)

            await self.session.commit()
            await self.session.refresh(user_db)
            return UserResponse.model_validate(user_db)

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при Обновление пользователя: {str(e)}"
            )