from fastapi import APIRouter, Depends, status, HTTPException

from api.deps import get_todo_service, get_user_token
from core.schems.token import TokenData
from core.service.task import TaskService
from core.schems.task import TaskBase, TaskCreate, TaskResponse, TaskUpdate
router = APIRouter()

@router.get(
    "/tasks",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_tasks(
    token_data: TokenData = Depends(get_user_token),
    service: TaskService  = Depends(get_todo_service)
):
    tasks = await service.get_tasks(token_data.sub)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У вас нет задач =)"
        )
    return tasks

@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_todo_service),
    token_data: TokenData = Depends(get_user_token)
) -> TaskResponse:
    new_task = await service.create_task(
        task=task,
        user_id=token_data.sub
    )
    if not new_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать задачу"
        )
    return new_task

@router.get(
    "/tasks/{task_id}"
)
async def get_task(
    task_id: int,
    token_data: TokenData = Depends(get_user_token),
    service: TaskService = Depends(get_todo_service)
):
    pass