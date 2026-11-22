import pytest
from unittest.mock import MagicMock

from app.exceptions.task_exceptions import TaskNotFoundError
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService


def make_service():
    repository = MagicMock(spec=TaskRepository)
    service = TaskService(repository)
    return repository, service


def make_task():
    return TaskResponse(
        id=1,
        title="Task 1",
        description="Description 1",
        completed=False,
    )


def test_create_task_success():
    repository, service = make_service()
    task_data = TaskCreate(title="Task 1", description="Description 1")
    repository.create.return_value = make_task()

    task = service.create_task(task_data)
    assert task == make_task()
    assert task.title == "Task 1"
    repository.create.assert_called_once_with(task_data)


def test_get_tasks():
    repository, service = make_service()
    repository.get_all.return_value = [make_task()]

    tasks = service.get_tasks()
    assert tasks == [make_task()]
    assert len(tasks) == 1
    assert tasks[0].title == "Task 1"
    repository.get_all.assert_called_once_with()


def test_get_task_success():
    repository, service = make_service()
    repository.get_by_id.return_value = make_task()

    task = service.get_task(1)

    # El servicio devuelve TaskResponse, no un diccionario.
    assert isinstance(task, TaskResponse)
    assert task.id == 1
    repository.get_by_id.assert_called_once_with(1)


def test_get_task_not_found():
    repository, service = make_service()
    repository.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError, match="Task not found"):
        service.get_task(999)


def test_delete_task_success():
    repository, service = make_service()
    repository.delete.return_value = True

    service.delete_task(1)

    repository.delete.assert_called_once_with(1)


def test_delete_task_not_found():
    repository, service = make_service()
    repository.delete.return_value = False

    with pytest.raises(TaskNotFoundError, match="Task not found"):
        service.delete_task(999)


def test_update_task_success():
    repository, service = make_service()
    task_data = TaskUpdate(title="Updated Task")
    updated_task = TaskResponse(
        id=1,
        title="Updated Task",
        description="Description 1",
        completed=False,
    )
    repository.update.return_value = updated_task

    task = service.update_task(1, task_data)
    assert task == updated_task
    assert task.title == "Updated Task"
    repository.update.assert_called_once_with(1, task_data)


def test_update_task_not_found():
    repository, service = make_service()
    task_data = TaskUpdate(title="Updated Task")
    repository.update.return_value = None

    with pytest.raises(TaskNotFoundError, match="Task not found"):
        service.update_task(999, task_data)