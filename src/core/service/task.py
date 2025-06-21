from repository.database.task import TaskRepository
from core.schems.task import TaskResponse, TaskBase, TaskCreate, TaskUpdate
from core.models.task import Task

class TaskService:
    def __init__(
        self,
        repository: TaskRepository
    ):
        self.repository = repository
    
    async def get_tasks(
        self, 
        user_id: int
    ) -> list[TaskResponse]:
        tasks = await self.repository.get_all_tasks(user_id=user_id)
        if not tasks:
            return []
        return [TaskResponse.from_orm(task) for task in tasks]


    async def get_one_task(
        self,
        user_id: int,
        task_id: int
    ) -> TaskResponse:
        pass

    async def create_task(
        self, 
        task: TaskCreate,
        user_id: int
    ) -> TaskResponse:
        task_dict = task.dict()
        task_dict.update(owner_id=user_id)
        new_task = await self.repository.create_task(Task(**task_dict))
        if not new_task:
            return None
        return TaskResponse.from_orm(new_task)

    async def update_task(
        self,
        task_id: int,
        task: TaskUpdate,
        user_id: int
    ) -> TaskResponse:
        new_task = await self.repository.update_task(task_id, task.dict())    
        if not new_task:
            return None
        return TaskResponse.from_orm(new_task)

    async def delete_task(
        self,
        task_id: int,
        user_id: int
    ) -> bool:
        return await self.repository.delete_task(
            task_id=task_id, 
            user_id=user_id
        )