from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  — register SQLModel tables before create_all
from app.database import init_db
from app.routers import auth_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="collab-notes", lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(users_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}
