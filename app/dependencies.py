

from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

# Una instancia compartida para mantener los datos en memoria
repository = TaskRepository()


def get_task_repository() -> TaskRepository:
    return repository


def get_task_service() -> TaskService:
    return TaskService(repository=get_task_repository())