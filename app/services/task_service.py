from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.exceptions.task_exceptions import TaskNotFoundError   


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        return self.repository.create(task_data)

    def get_tasks(self) -> list[TaskResponse]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> TaskResponse:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError("Task not found")
        return task

    def delete_task(self, task_id: int) -> None:
        if not self.repository.delete(task_id):
            raise TaskNotFoundError("Task not found")

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate
    ) -> TaskResponse:
        task = self.repository.update(task_id, task_data)
        if task is None:
            raise TaskNotFoundError("Task not found")
        return task