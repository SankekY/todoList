from repository.database.user import UserRepository
from core.schems.user import UserCreate, UserResponse, UserBase, UserUpdate


class UserService:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository
    
    pass

    def create_user(self, user: UserCreate) -> UserResponse:
        return self.create_user(user)

    def get_user(self, user: UserBase) -> UserResponse:
        pass