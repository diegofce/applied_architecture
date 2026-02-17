from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend package is importable in local runs and Vercel runtime.
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_SRC = CURRENT_DIR.parent / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.append(str(BACKEND_SRC))

from todo_app.application.interfaces.validators import CreateTaskCommand, UpdateTaskCommand
from todo_app.infrastructure.factories.service_factory import DefaultServiceFactory
from todo_app.presentation.schemas.task_schema import (
    ErrorResponse,
    TaskCreateRequest,
    TaskResponse,
    TaskStatusRequest,
    TaskUpdateRequest,
)

app = FastAPI(title="Monolith To-Do API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

factory = DefaultServiceFactory()
service = factory.task_service()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    return [TaskResponse(**task.__dict__) for task in service.list_tasks()]


@app.post("/api/tasks", response_model=TaskResponse, responses={400: {"model": ErrorResponse}})
def create_task(payload: TaskCreateRequest) -> TaskResponse:
    try:
        task = service.create_task(
            CreateTaskCommand(title=payload.title, description=payload.description)
        )
        return TaskResponse(**task.__dict__)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/tasks/{task_id}", response_model=TaskResponse, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
def update_task(task_id: str, payload: TaskUpdateRequest) -> TaskResponse:
    try:
        task = service.update_task(
            UpdateTaskCommand(task_id=task_id, title=payload.title, description=payload.description)
        )
        return TaskResponse(**task.__dict__)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.patch("/api/tasks/{task_id}/status", response_model=TaskResponse, responses={404: {"model": ErrorResponse}})
def patch_task_status(task_id: str, payload: TaskStatusRequest) -> TaskResponse:
    try:
        task = service.set_completed(task_id=task_id, completed=payload.completed)
        return TaskResponse(**task.__dict__)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.delete("/api/tasks/{task_id}", status_code=204, responses={404: {"model": ErrorResponse}})
def delete_task(task_id: str) -> None:
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found.")
