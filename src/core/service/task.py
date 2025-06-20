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
        db_tasks_list = await self.repository.get_all_tasks(user_id=user_id)
        if not db_tasks_list:
            return None
        response_list = []
        for db_task in db_tasks_list:
            response_list.append(TaskResponse.from_orm(db_task))
        return response_list
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

    async def task_update(
        self, 
        task_id: int,
        user_id: int, 
        task_update: TaskUpdate
    ) -> TaskResponse:
        pass

    async def delete_task(
        self, 
        task_id: int,
        user_id: int
    ):
        pass