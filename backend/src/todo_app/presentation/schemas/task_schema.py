from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None


class TaskUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = None


class TaskStatusRequest(BaseModel):
    completed: bool


class TaskResponse(BaseModel):
    id: str
    title: str
    completed: bool
    description: str | None
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str
