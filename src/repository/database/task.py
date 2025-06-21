
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

import logging
from repository.database.base import BaseRepository
from core.models.task import Task

class TaskRepository(BaseRepository[Task]):
    
    async def create_task(self, task: Task) -> Task:
        try:
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            return task
        except SQLAlchemyError as e:
            logging.error(f"Error creating task: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected error in create_task: {str(e)}")
            return None

    async def get_all_tasks(self, user_id: int) -> list[Task]:
        try:
            query = select(Task).where(Task.owner_id == user_id)
            result = await self.session.execute(query)
            tasks = result.scalars().all()
            
            return tasks if tasks else []
            
        except SQLAlchemyError as e:
            logging.error(f"Error fetching tasks for user {user_id}: {str(e)}")
            return []
        except Exception as e:
            logging.critical(f"Unexpected error in get_all_tasks: {str(e)}")
            return []
    
    async def get_task_by_id(self, task_id: int, user_id: int) -> Task:
        try:
            query = select(Task).where(Task.id == task_id)
            result = await self.session.execute(query)
            task = result.scalar_one_or_none()
            if not task:
                return None
            if task.owner_id != user_id:
                return None
            return task
            
        except SQLAlchemyError as e:
            logging.error(f"Error fetching task {task_id}: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected error in get_task_by_id: {str(e)}")
            return None

    async def update_task(self, task_id: int, task_data: dict, user_id: int) -> Task:
        try:
            task = await self.get_task_by_id(task_id=task_id, user_id=user_id)
            if not task:
                return None
            for key, value in task_data.items():
                if value is not None:
                    setattr(task, key, value)
            await self.session.commit()
            await self.session.refresh(task)

            return task
            
        except SQLAlchemyError as e:
            logging.error(f"Error updating task {task_id}: {str(e)}")
            return None
        except Exception as e:
            logging.critical(f"Unexpected error in update_task: {str(e)}")
            return None

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        try:
            task = await self.get_task_by_id(task_id=task_id, user_id=user_id)
            if not task:
                return False
            await self.session.delete(task)
            await self.session.commit()
            return True

        except SQLAlchemyError as e:
            logging.error(f"Error deleting task {task_id}: {str(e)}")
            return False
        except Exception as e:
            logging.critical(f"Unexpected error in delete_task: {str(e)}")
            return False