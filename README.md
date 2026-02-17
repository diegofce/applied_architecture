# Applied Architecture - FullStack To-Do Monolith

Aplicacion Full Stack de gestion de tareas con enfoque en arquitectura de software en Python.

Stack:
- Backend: FastAPI (Python)
- Frontend: React + Vite
- Persistencia: SQLAlchemy + PostgreSQL (Neon/Supabase/RDS) o SQLite local
- Deploy: Vercel (frontend + serverless Python API)

## Objetivo tecnico

Este proyecto prioriza calidad de diseno sobre complejidad funcional:
- separacion por capas
- contratos abstractos
- principios SOLID
- patrones de diseno aplicados en codigo real

## Arquitectura

Estructura principal:
- `api/index.py`: entrypoint ASGI para Vercel
- `backend/src/todo_app/domain`: entidades y contratos del dominio
- `backend/src/todo_app/application`: casos de uso y servicios de aplicacion
- `backend/src/todo_app/infrastructure`: implementaciones concretas (DB, factories, repositorios)
- `frontend/`: cliente React

Patrones implementados:
- Repository Pattern: `TaskRepository` + implementaciones (`SqlAlchemyTaskRepository`, `InMemoryTaskRepository`)
- Strategy Pattern: `TaskCommandValidator` + `BasicTaskCommandValidator`
- Abstract Factory: `ServiceFactory` + `DefaultServiceFactory`
- Dependency Inversion: `DefaultTaskService` depende de abstracciones, no de detalles

## Variables de entorno

- `TASK_REPOSITORY_PROVIDER`: `sqlalchemy` (default) o `memory`
- `DATABASE_URL`:
  - local default: `sqlite:///./tasks.db`
  - produccion (PostgreSQL): `postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require`

Notas:
- Si la URL viene como `postgres://...`, se normaliza automaticamente.
- En Vercel, si `TASK_REPOSITORY_PROVIDER=sqlalchemy` y falta `DATABASE_URL`, el backend falla intencionalmente para evitar datos efimeros.

## Ejecucion local

Requisitos:
- Python 3.11+
- Node.js 20+
- npm

### 1) Backend

En PowerShell (raiz del proyecto):

```powershell
Copy-Item .env.example .env
python -m pip install -r requirements.txt
$env:PYTHONPATH="backend/src"
python -m uvicorn api.index:app --reload --port 8000
```

Backend disponible en:
- `http://localhost:8000/api/health`
- `http://localhost:8000/api/tasks`

### 2) Frontend

En otra terminal (raiz del proyecto):

```powershell
cmd /c npm install --prefix frontend
cmd /c npm run dev --prefix frontend
```

Frontend disponible en:
- `http://localhost:5173`

## Deploy en Vercel

1. Sube este proyecto a GitHub.
2. Importa el repo en Vercel.
3. Configura variables de entorno del proyecto:
   - `TASK_REPOSITORY_PROVIDER=sqlalchemy`
   - `DATABASE_URL=<postgres_url_con_ssl>`
4. Ejecuta deploy.

Opcional por CLI:

```bash
vercel login
vercel
vercel --prod
```

`vercel.json` ya incluye:
- build de frontend Vite
- runtime Python para `api/index.py`
- rewrites para `/api/*` y SPA

## Deploy en Railway (backend)

Este repo ya incluye `railway.toml` con el comando de arranque.

1. Sube el repo a GitHub y crea un proyecto en Railway.
2. En **Settings > Variables**, configura:
   - `TASK_REPOSITORY_PROVIDER=sqlalchemy`
   - `DATABASE_URL=<postgres_url_con_ssl>`
3. En **Deployments**, ejecuta el primer deploy.

Notas:
- El backend expone `/api/health`.
- El comando de arranque es `uvicorn api.index:app --host 0.0.0.0 --port $PORT`.

## API

- `GET /api/health`
- `GET /api/tasks`
- `POST /api/tasks`
- `PUT /api/tasks/{task_id}`
- `PATCH /api/tasks/{task_id}/status`
- `DELETE /api/tasks/{task_id}`

## Checklist de validacion

Pre-deploy:
- `python -m pip install -r requirements.txt` OK
- `cmd /c npm install --prefix frontend` OK
- `python -m uvicorn api.index:app --reload --port 8000` responde `200` en `/api/health`
- `cmd /c npm run build --prefix frontend` termina en `built`
- CRUD local retorna 200/204

Post-deploy:
- `GET https://<dominio>/api/health` -> `{"status":"ok"}`
- crear tarea desde UI
- recargar y confirmar persistencia (DB remota conectada)

## Roadmap tecnico

- Autenticacion JWT + autorizacion por usuario
- CORS estricto por entorno
- Rate limiting
- Logging estructurado y trazabilidad
- Tests unitarios/integracion + CI (GitHub Actions)
- Migraciones con Alembic
