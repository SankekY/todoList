from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import get_session, get_user_service, get_user_token, get_todo_service
from core.schems.user import UserResponse, UserCreate, UserBase, UserUpdate, UserTokenData, UserWithTasks
from core.schems.token import Token, TokenData
from core.service.user import UserService
from core.schems.task import TaskBase, TaskResponse
from core.service.task import TaskService

router = APIRouter(
)

@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK
)
async def get_access_token(
    user_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
) -> Token:
    token =  await service.login_user(UserUpdate(
        password=user_data.password,
        username=user_data.username
    ))
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не верный логин или пароль!"
        )
    return token

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def register_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    new_user = await service.create_user(user)
    if new_user == None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой пользователь уже зарегестрирован"
        )
    return new_user

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_me(
    token_data: TokenData = Depends(get_user_token),
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user(UserBase(
        username=token_data.username,
        email=token_data.email
    ))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удолось получить данные с сервера!"
        )
    return user


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    user: UserUpdate,
    token_data: TokenData = Depends(get_user_token),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    
    new_user = await service.update_user(user, int(token_data.sub))
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновление польтзователя"
        )
    return new_user

@router.get(
    "/{user_id}/tasks",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_tasks(
    user_id: int,
    service: UserService = Depends(get_user_service), 
    task_service: TaskService = Depends(get_todo_service)
) -> UserResponse:
    user = await service.get_user_by_id(id=user_id)
    tasks = await task_service.get_tasks(user_id=user_id)
    if not user or not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    user.tasks = tasks
    return UserWithTasks(**user.dict())