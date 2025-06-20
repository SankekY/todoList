from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import get_session, get_user_service, get_user_token
from core.schems.user import UserResponse, UserCreate, UserBase, UserUpdate, UserTokenData
from core.schems.token import Token, TokenData
from core.service.user import UserService

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