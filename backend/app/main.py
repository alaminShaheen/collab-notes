from fastapi import FastAPI

from app.routers import auth_router, users_router

app = FastAPI(title="collab-notes")

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
