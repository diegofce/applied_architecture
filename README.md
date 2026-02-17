# FullStack To-Do Monolito (Python + React)

Arquitectura enfocada en clases abstractas, SOLID y patrones de diseno.

## Estructura

- `api/index.py`: FastAPI entrypoint para Vercel
- `backend/src/todo_app/domain`: entidades y contratos abstractos
- `backend/src/todo_app/application`: casos de uso
- `backend/src/todo_app/infrastructure`: implementaciones concretas
- `frontend`: React + Vite

## Patrones y SOLID aplicados

- Repository Pattern: `TaskRepository` + `SqlAlchemyTaskRepository` / `InMemoryTaskRepository`
- Strategy Pattern: `TaskCommandValidator` + `BasicTaskCommandValidator`
- Abstract Factory: `ServiceFactory` + `DefaultServiceFactory`
- DIP/SRP en `DefaultTaskService`
- Entidad de dominio inmutable `Task`

## Variables de entorno

- `TASK_REPOSITORY_PROVIDER`: `sqlalchemy` (default) o `memory`
- `DATABASE_URL`: por defecto `sqlite:///./tasks.db`

Para PostgreSQL (local o Vercel), usa por ejemplo:

`DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME`

Tambien soporta URL estilo `postgres://...` y se normaliza automaticamente.

## Requisitos

- Python 3.11+
- Node.js 20+
- npm

## Ejecucion local

### 1) Backend

PowerShell en raiz:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "backend/src"
# Recomendado: SQLite local
$env:TASK_REPOSITORY_PROVIDER = "sqlalchemy"
# Opcional: para Postgres local/remoto
# $env:DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME"
python -m uvicorn api.index:app --reload --port 8000
```

API en `http://localhost:8000/api/tasks`.

### 2) Frontend

Otra terminal:

```powershell
cmd /c npm install --prefix frontend
cmd /c npm run dev --prefix frontend
```

Frontend en `http://localhost:5173`.

### Troubleshooting backend local

- Si `uvicorn` no se reconoce, usa siempre `python -m uvicorn ...`.
- Si falla `npm` en PowerShell por policy, usa `cmd /c npm ...`.
- Verifica backend con:
```powershell
Invoke-RestMethod http://localhost:8000/api/health
```
- Verifica CRUD rapido:
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/tasks -ContentType application/json -Body '{"title":"test"}'
Invoke-RestMethod http://localhost:8000/api/tasks
```

## Deploy en Vercel

1. Sube este proyecto a GitHub.
2. En Vercel, importa el repo.
3. En Variables de Entorno del proyecto agrega:
   - `TASK_REPOSITORY_PROVIDER=sqlalchemy`
   - `DATABASE_URL=<tu_url_postgresql>` (Neon/Supabase/RDS)
4. Deploy.

`vercel.json` ya define:
- build frontend con Vite
- runtime Python para `api/index.py`
- rewrites para `/api/*` y SPA
- Si `DATABASE_URL` no esta en Vercel y usas `sqlalchemy`, el backend fallara intencionalmente al iniciar.

## Endpoints

- `GET /api/health`
- `GET /api/tasks`
- `POST /api/tasks`
- `PUT /api/tasks/{task_id}`
- `PATCH /api/tasks/{task_id}/status`
- `DELETE /api/tasks/{task_id}`

## Checklist de validacion

### Antes de desplegar

- `python -m pip install -r requirements.txt` sin errores.
- `cmd /c npm install --prefix frontend` sin errores.
- `python -m uvicorn api.index:app --reload --port 8000` responde en `/api/health`.
- `cmd /c npm run build --prefix frontend` termina en `built`.
- CRUD local responde 200/204.

### Variables en Vercel

- `TASK_REPOSITORY_PROVIDER=sqlalchemy`.
- `DATABASE_URL` de Postgres valida y accesible.
- Base de datos con SSL habilitado (`sslmode=require` si el proveedor lo exige).

### Despues de desplegar

- `GET https://<tu-dominio>/api/health` retorna `{"status":"ok"}`.
- `POST https://<tu-dominio>/api/tasks` crea registro.
- `GET https://<tu-dominio>/api/tasks` devuelve la tarea creada.
- Recarga pagina y confirma persistencia (si persiste, DB remota esta correcta).
