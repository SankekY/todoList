from repository.database.base import BaseRepository
from core.models.user import User

class UserRepository(BaseRepository(User)):
    pass