from repository.database.user import UserRepository
from core.schems.user import UserCreate, UserResponse, UserBase, UserUpdate
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
            user = UserBase(
                username=user_db.username,
                email=user.email
            )
            return Token(
                access_token=encode_jwt(user.dict())
            )
        return None
        
        