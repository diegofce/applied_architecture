from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class Task:
    """Domain entity for tasks."""

    id: str
    title: str
    completed: bool = False
    description: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_completed(self) -> "Task":
        return replace(self, completed=True)

    def reopen(self) -> "Task":
        return replace(self, completed=False)

    def rename(self, new_title: str, new_description: Optional[str]) -> "Task":
        return replace(self, title=new_title, description=new_description)
