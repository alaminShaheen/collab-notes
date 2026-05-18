from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.mongo import get_database


class LogRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["logs"]

    async def insert(
        self,
        event_type: str,
        user_id: int,
        resource_id: str | None,
        metadata: dict[str, Any],
    ) -> None:
        await self.collection.insert_one(
            {
                "event_type": event_type,
                "user_id": user_id,
                "resource_id": resource_id,
                "timestamp": datetime.now(timezone.utc),
                "metadata": metadata,
            }
        )

    async def list(
        self,
        user_id: int | None = None,
        event_type: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {}
        if user_id is not None:
            query["user_id"] = user_id
        if event_type is not None:
            query["event_type"] = event_type

        cursor = (
            self.collection.find(query, {"_id": 0})
            .sort("timestamp", -1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_database)]


def get_log_repository(db: DatabaseDep) -> LogRepository:
    return LogRepository(db)
