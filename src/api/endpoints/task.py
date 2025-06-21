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
    if len(tasks) == 0:
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
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
async def get_task(
    task_id: int,
    token_data: TokenData = Depends(get_user_token),
    service: TaskService = Depends(get_todo_service)
):
    task = await service.get_one_task(
        task_id=task_id,
        user_id=int(token_data.sub)
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task 

@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    token_data: TokenData = Depends(get_user_token),
    service: TaskService = Depends(get_todo_service)
):
    new_taks = await service.update_task(
        task_id=task_id, 
        task=task_update, 
        user_id=token_data.sub
    )
    if not new_taks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return new_taks


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    token_data: TokenData = Depends(get_user_token),
    service: TaskService = Depends(get_todo_service)
):
    return await service.delete_task(
        task_id=task_id,
        user_id=token_data.sub
    )