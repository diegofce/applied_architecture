from threading import Lock
from typing import Optional

from todo_app.domain.entities.task import Task
from todo_app.domain.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    """Thread-safe in-memory repository for demo and local use."""

    def __init__(self) -> None:
        self._data: dict[str, Task] = {}
        self._lock = Lock()

    def list_all(self) -> list[Task]:
        with self._lock:
            return sorted(self._data.values(), key=lambda t: t.created_at, reverse=True)

    def get_by_id(self, task_id: str) -> Optional[Task]:
        with self._lock:
            return self._data.get(task_id)

    def save(self, task: Task) -> Task:
        with self._lock:
            self._data[task.id] = task
            return task

    def delete(self, task_id: str) -> bool:
        with self._lock:
            existed = task_id in self._data
            if existed:
                del self._data[task_id]
            return existed
