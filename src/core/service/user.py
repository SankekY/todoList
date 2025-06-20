from repository.database.user import UserRepository
from core.schems.user import UserCreate, UserResponse, UserBase, UserUpdate, UserTokenData
from utils.auth_jwt  import verefy_passowrd, decode_jwt, encode_jwt
from core.schems.token import Token, TokenData


class UserService:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def create_user(self, user: UserCreate) -> UserResponse:
        return await self.repository.create_user(user)

    async def login_user(self, user: UserUpdate) -> Token:
        user_db = await self.repository.get_user(user)
        if not user_db: 
            return None
        if verefy_passowrd(user.password, user_db.password_hash):
            user_data = UserTokenData.model_validate(user_db)
            return Token(
                access_token=encode_jwt(TokenData(
                    sub=str(user_db.id),
                    username=user_db.username,
                    email=user_db.email,
                    active=user_db.is_active
                ).dict())
            )
        return None
        
    async def get_user(self, user: UserBase) -> UserResponse:
        user_db = await self.repository.get_user(user)
        if not user_db:
            return None
        return UserResponse.model_validate(user_db)

    async def update_user(self, new_user: UserUpdate, id: int) -> UserResponse:
        user_db = await self.repository.update_user(new_user, id)
        if not user_db:
            return None
        if user_db.id != id:
            return None
        return UserResponse.model_validate(user_db)
        