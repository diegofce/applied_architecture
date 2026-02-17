from datetime import timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from todo_app.domain.entities.task import Task
from todo_app.domain.repositories.task_repository import TaskRepository
from todo_app.infrastructure.database.models import TaskRecord


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def list_all(self) -> list[Task]:
        with self._session_factory() as session:
            statement = select(TaskRecord).order_by(TaskRecord.created_at.desc())
            records = session.execute(statement).scalars().all()
            return [self._to_domain(record) for record in records]

    def get_by_id(self, task_id: str) -> Optional[Task]:
        with self._session_factory() as session:
            record = session.get(TaskRecord, task_id)
            return self._to_domain(record) if record else None

    def save(self, task: Task) -> Task:
        with self._session_factory() as session:
            record = session.get(TaskRecord, task.id)
            if record is None:
                record = TaskRecord(
                    id=task.id,
                    title=task.title,
                    completed=task.completed,
                    description=task.description,
                    created_at=task.created_at,
                )
                session.add(record)
            else:
                record.title = task.title
                record.completed = task.completed
                record.description = task.description
            session.commit()
            session.refresh(record)
            return self._to_domain(record)

    def delete(self, task_id: str) -> bool:
        with self._session_factory() as session:
            record = session.get(TaskRecord, task_id)
            if record is None:
                return False
            session.delete(record)
            session.commit()
            return True

    @staticmethod
    def _to_domain(record: TaskRecord) -> Task:
        created_at = record.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        return Task(
            id=record.id,
            title=record.title,
            completed=record.completed,
            description=record.description,
            created_at=created_at,
        )
