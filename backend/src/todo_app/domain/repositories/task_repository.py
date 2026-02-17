from abc import ABC, abstractmethod
from typing import Optional

from todo_app.domain.entities.task import Task


class TaskRepository(ABC):
    """Repository pattern abstraction (DIP)."""

    @abstractmethod
    def list_all(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        raise NotImplementedError

    @abstractmethod
    def save(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        raise NotImplementedError
