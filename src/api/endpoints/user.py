from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import get_session, get_user_service

from core.schems.user import UserResponse, UserCreate, UserBase, UserUpdate
from core.schems.token import Token
from core.service.user import UserService

router = APIRouter()

@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK
)
async def get_access_token(
    user_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
) -> Token:
    return Token

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def register_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await service.create_user(user)