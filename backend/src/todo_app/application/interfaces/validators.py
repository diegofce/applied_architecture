from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str | None = None


@dataclass(frozen=True)
class UpdateTaskCommand:
    task_id: str
    title: str
    description: str | None = None


class TaskCommandValidator(ABC):
    """Strategy abstraction for command validation."""

    @abstractmethod
    def validate_create(self, command: CreateTaskCommand) -> None:
        raise NotImplementedError

    @abstractmethod
    def validate_update(self, command: UpdateTaskCommand) -> None:
        raise NotImplementedError
