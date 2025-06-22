from api.endpoints.user import router as user_router
from api.endpoints.task import router as task_router
from fastapi import APIRouter

main_router = APIRouter(
    prefix="/api", 
)
main_router.include_router(user_router, tags=["User"])
main_router.include_router(task_router, tags=["Task"])
