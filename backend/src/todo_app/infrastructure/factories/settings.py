import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    repository_provider: str
    database_url: str
    is_vercel: bool


class SettingsFactory:
    @staticmethod
    def load() -> DatabaseSettings:
        provider = os.getenv("TASK_REPOSITORY_PROVIDER", "sqlalchemy").strip().lower()
        is_vercel = bool(os.getenv("VERCEL"))
        database_url = os.getenv("DATABASE_URL", "").strip()

        if provider == "sqlalchemy":
            if is_vercel and not database_url:
                raise ValueError(
                    "DATABASE_URL is required in Vercel when TASK_REPOSITORY_PROVIDER=sqlalchemy."
                )
            if not database_url:
                database_url = "sqlite:///./tasks.db"

        return DatabaseSettings(
            repository_provider=provider, database_url=database_url, is_vercel=is_vercel
        )
