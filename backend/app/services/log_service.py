from typing import Annotated

from fastapi import Depends

from app.repositories.log_repo import LogRepository, get_log_repository


class LogService:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo

    async def user_signup(self, user_id: int, username: str) -> None:
        await self.log_repo.insert(
            "user_signup", user_id, None, {"username": username}
        )

    async def user_login(self, user_id: int, username: str) -> None:
        await self.log_repo.insert(
            "user_login", user_id, None, {"username": username}
        )

    async def note_created(self, user_id: int, note_id: str, title: str) -> None:
        await self.log_repo.insert(
            "note_created", user_id, note_id, {"title": title}
        )

    async def note_updated(
        self, user_id: int, note_id: str, fields_updated: list[str]
    ) -> None:
        await self.log_repo.insert(
            "note_updated", user_id, note_id, {"fields_updated": fields_updated}
        )

    async def note_deleted(self, user_id: int, note_id: str, title: str) -> None:
        await self.log_repo.insert(
            "note_deleted", user_id, note_id, {"title": title}
        )

    async def note_searched(self, user_id: int, query: str) -> None:
        await self.log_repo.insert(
            "note_searched", user_id, None, {"query": query}
        )

    async def list(
        self,
        user_id: int | None = None,
        event_type: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[dict]:
        return await self.log_repo.list(user_id, event_type, limit, skip)


LogRepoDep = Annotated[LogRepository, Depends(get_log_repository)]


def get_log_service(log_repo: LogRepoDep) -> LogService:
    return LogService(log_repo)
