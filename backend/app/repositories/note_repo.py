from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.mongo import get_database
from app.schemas.note import NoteCreate


class NoteRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["notes"]

    @staticmethod
    def _to_object_id(note_id: str) -> ObjectId | None:
        try:
            return ObjectId(note_id)
        except (InvalidId, TypeError):
            return None

    @staticmethod
    def _serialize(doc: dict) -> dict:
        doc["id"] = str(doc.pop("_id"))
        return doc

    async def create(self, owner_id: int, payload: NoteCreate) -> dict:
        now = datetime.now(timezone.utc)
        doc = {
            "owner_id": owner_id,
            "title": payload.title,
            "content": payload.content,
            "created_at": now,
            "updated_at": now,
        }
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return self._serialize(doc)

    async def list_by_owner(self, owner_id: int) -> list[dict]:
        cursor = self.collection.find({"owner_id": owner_id}).sort("updated_at", -1)
        return [self._serialize(doc) async for doc in cursor]

    async def get_for_owner(self, note_id: str, owner_id: int) -> dict | None:
        oid = self._to_object_id(note_id)
        if oid is None:
            return None
        doc = await self.collection.find_one({"_id": oid, "owner_id": owner_id})
        return self._serialize(doc) if doc else None

    async def replace_for_owner(
        self, note_id: str, owner_id: int, payload: NoteCreate
    ) -> dict | None:
        oid = self._to_object_id(note_id)
        if oid is None:
            return None

        doc = await self.collection.find_one_and_update(
            {"_id": oid, "owner_id": owner_id},
            {
                "$set": {
                    "title": payload.title,
                    "content": payload.content,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
            return_document=ReturnDocument.AFTER,
        )
        return self._serialize(doc) if doc else None

    async def delete_for_owner(self, note_id: str, owner_id: int) -> bool:
        oid = self._to_object_id(note_id)
        if oid is None:
            return False
        result = await self.collection.delete_one({"_id": oid, "owner_id": owner_id})
        return result.deleted_count > 0


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_database)]


def get_note_repository(db: DatabaseDep) -> NoteRepository:
    return NoteRepository(db)
