from abc import ABC, abstractmethod

from todo_app.application.use_cases.task_service import DefaultTaskService, TaskService
from todo_app.infrastructure.database.bootstrap import initialize_database
from todo_app.infrastructure.database.session import build_session_factory
from todo_app.infrastructure.factories.id_generator_factory import UUIDGenerator
from todo_app.infrastructure.factories.settings import SettingsFactory
from todo_app.infrastructure.factories.validators import BasicTaskCommandValidator
from todo_app.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from todo_app.infrastructure.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository


class ServiceFactory(ABC):
    """Abstract Factory for wiring dependencies."""

    @abstractmethod
    def task_service(self) -> TaskService:
        raise NotImplementedError


class DefaultServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        settings = SettingsFactory.load()
        self._repository = self._build_repository(
            provider=settings.repository_provider,
            database_url=settings.database_url,
        )
        self._id_generator = UUIDGenerator()
        self._validator = BasicTaskCommandValidator()
        self._task_service = DefaultTaskService(
            repository=self._repository,
            id_generator=self._id_generator,
            validator=self._validator,
        )

    def task_service(self) -> TaskService:
        return self._task_service

    @staticmethod
    def _build_repository(provider: str, database_url: str):
        if provider == "memory":
            return InMemoryTaskRepository()

        if provider == "sqlalchemy":
            session_factory = build_session_factory(database_url)
            initialize_database(session_factory)
            return SqlAlchemyTaskRepository(session_factory)

        raise ValueError(
            "Unsupported TASK_REPOSITORY_PROVIDER. Use 'sqlalchemy' or 'memory'."
        )
