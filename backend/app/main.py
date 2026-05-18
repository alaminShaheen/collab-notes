from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  — register SQLModel tables before create_all
from app.database import init_db
from app.elasticsearch import connect_to_elasticsearch, close_elasticsearch_connection
from app.mongo import close_mongo_connection, connect_to_mongo
from app.routers import auth_router, logs_router, notes_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    await connect_to_mongo()
    await connect_to_elasticsearch()
    try:
        yield
    finally:
        await close_elasticsearch_connection()
        await close_mongo_connection()


app = FastAPI(title="collab-notes", lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(notes_router.router)
app.include_router(logs_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}
