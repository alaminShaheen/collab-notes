from sqlmodel import create_engine, SQLModel, Session

from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    """Create all tables. For dev only — use Alembic for prod migrations."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency — yields a session, closes it after the request."""
    with Session(engine) as session:
        yield session