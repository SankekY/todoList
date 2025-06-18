from repository.database.base import BaseRepository
from core.models.task import Task

class TaskRepository(BaseRepository(Task)):
    pass