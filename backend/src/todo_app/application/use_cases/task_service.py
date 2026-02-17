from abc import ABC, abstractmethod
from datetime import datetime, timezone

from todo_app.application.interfaces.validators import (
    CreateTaskCommand,
    TaskCommandValidator,
    UpdateTaskCommand,
)
from todo_app.domain.entities.task import Task
from todo_app.domain.repositories.task_repository import TaskRepository
from todo_app.domain.services.id_generator import IdGenerator


class TaskService(ABC):
    @abstractmethod
    def list_tasks(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def create_task(self, command: CreateTaskCommand) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, command: UpdateTaskCommand) -> Task:
        raise NotImplementedError

    @abstractmethod
    def set_completed(self, task_id: str, completed: bool) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        raise NotImplementedError


class DefaultTaskService(TaskService):
    """Application service using dependency inversion for repository/validators/ID generation."""

    def __init__(
        self,
        repository: TaskRepository,
        id_generator: IdGenerator,
        validator: TaskCommandValidator,
    ) -> None:
        self._repository = repository
        self._id_generator = id_generator
        self._validator = validator

    def list_tasks(self) -> list[Task]:
        return self._repository.list_all()

    def create_task(self, command: CreateTaskCommand) -> Task:
        self._validator.validate_create(command)
        task = Task(
            id=self._id_generator.next_id(),
            title=command.title.strip(),
            description=self._normalize_description(command.description),
            created_at=datetime.now(timezone.utc),
        )
        return self._repository.save(task)

    def update_task(self, command: UpdateTaskCommand) -> Task:
        self._validator.validate_update(command)
        existing = self._repository.get_by_id(command.task_id)
        if existing is None:
            raise KeyError("Task not found.")
        updated = existing.rename(command.title.strip(), self._normalize_description(command.description))
        return self._repository.save(updated)

    def set_completed(self, task_id: str, completed: bool) -> Task:
        existing = self._repository.get_by_id(task_id)
        if existing is None:
            raise KeyError("Task not found.")
        updated = existing.mark_completed() if completed else existing.reopen()
        return self._repository.save(updated)

    def delete_task(self, task_id: str) -> bool:
        return self._repository.delete(task_id)

    @staticmethod
    def _normalize_description(description: str | None) -> str | None:
        if description is None:
            return None
        clean = description.strip()
        return clean if clean else None
