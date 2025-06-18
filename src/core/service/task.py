from repository.database.task import TaskRepository


class TaskService:
    def __init__(
        self,
        repository: TaskRepository
    ):
        self.repository = repository
    
    pass