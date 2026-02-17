from todo_app.application.interfaces.validators import (
    CreateTaskCommand,
    TaskCommandValidator,
    UpdateTaskCommand,
)


class BasicTaskCommandValidator(TaskCommandValidator):
    def validate_create(self, command: CreateTaskCommand) -> None:
        self._validate_title(command.title)

    def validate_update(self, command: UpdateTaskCommand) -> None:
        if not command.task_id.strip():
            raise ValueError("Task ID is required.")
        self._validate_title(command.title)

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Task title is required.")
        if len(title.strip()) > 120:
            raise ValueError("Task title must be <= 120 characters.")
