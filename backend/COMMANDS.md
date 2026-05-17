# collab-notes backend — command reference

All commands run from `backend/` unless noted. Activate the venv first.

## venv

```powershell
# Activate (PowerShell)
.venv\Scripts\Activate.ps1

# Activate (cmd.exe)
.venv\Scripts\activate.bat

# Deactivate
deactivate

# Recreate from scratch
deactivate

Remove-Item -Recurse -Force .venv
py -m venv .venv
.venv\Scripts\Activate.ps1
```

## Dependencies

```bash
pip install -r requirements.txt          # install everything
pip install <pkg>                        # add a new package
pip freeze > requirements.txt            # pin current versions (do before deploy)
```

## Docker (Postgres + Mongo)

```bash
docker compose up -d                     # start containers in background
docker compose down                      # stop containers (keep data)
docker compose down -v                   # stop + WIPE volumes (destroys data)
docker compose ps                        # show running services (look for "healthy")
docker compose logs -f                   # tail all logs
docker compose logs -f postgres          # tail just one service
docker compose restart postgres          # restart one service
```

### Direct psql access

```bash
docker exec -it collab-notes-pg psql -U postgres -d collab_notes

# Inside psql:
\dt                                      # list tables
\d users                                 # describe a table
\l                                       # list databases
\q                                       # quit
```

## Alembic (migrations)

```bash
alembic revision --autogenerate -m "msg" # generate migration from model changes
alembic upgrade head                     # apply all pending migrations
alembic upgrade +1                       # apply just the next one
alembic downgrade -1                     # undo the last migration
alembic downgrade base                   # undo everything
alembic current                          # what revision is the DB on
alembic history                          # full list of migrations
alembic show <revision_id>               # details of one revision
```

**Workflow when changing a model:**
1. Edit `app/models/*.py`
2. `alembic revision --autogenerate -m "what changed"`
3. **Read the generated file in `alembic/versions/`** — autogenerate isn't perfect
4. `alembic upgrade head`
5. Commit model change + migration file together

## FastAPI server

```bash
uvicorn app.main:app --reload            # dev mode, auto-reload on file change
uvicorn app.main:app --host 0.0.0.0 --port 8000   # bind to all interfaces
```

- API docs (Swagger): http://localhost:8000/docs
- API docs (ReDoc): http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Quick sanity checks

```bash
# DB connection from Python
python -c "from sqlmodel import Session, text; from app.database import engine; print(Session(engine).exec(text('SELECT version()')).first())"

# Container reachable on host
docker exec -it collab-notes-pg pg_isready -U postgres
```
