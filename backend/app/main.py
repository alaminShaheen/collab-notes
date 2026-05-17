from fastapi import FastAPI

from app.routers import auth, users

app = FastAPI(title="collab-notes")

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
