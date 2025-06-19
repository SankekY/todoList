from api.endpoints.user import router as user_router
from api.endpoints.task import router as task_router
from fastapi import APIRouter

main_router = APIRouter(
    prefix="/api",
    tags=["TodoTasks"]
)
main_router.include_router(user_router)
main_router.include_router(task_router)
