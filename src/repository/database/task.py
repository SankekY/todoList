from sqlalchemy import select

from repository.database.base import BaseRepository
from core.models.task import Task

class TaskRepository(BaseRepository[Task]):
    
    async def create_task(self, task: Task) -> Task:
        try:
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            return task

        except Exception as e:
            return None

    async def get_all_tasks(self, user_id: int) -> list[Task] | None:
        try:
            query = select(Task).where(Task.owner_id == user_id)
            result = await self.session.execute(query)
            tasks = result.scalars().all()
            
            return tasks if tasks else None
            
        except SQLAlchemyError as e:
            logging.error(f"Error fetching tasks for user {user_id}: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected error in get_all_tasks: {str(e)}")
            return None
    