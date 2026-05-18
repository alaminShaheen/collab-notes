from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models import User
from app.repositories.note_repo import NoteRepository, get_note_repository
from app.schemas.note import NoteCreate


class NoteService:
    def __init__(self, note_repo: NoteRepository):
        self.note_repo = note_repo

    async def create(self, user: User, payload: NoteCreate) -> dict:
        return await self.note_repo.create(user.id, payload)

    async def list_for_user(self, user: User) -> list[dict]:
        return await self.note_repo.list_by_owner(user.id)

    async def get(self, user: User, note_id: str) -> dict:
        note = await self.note_repo.get_for_owner(note_id, user.id)
        if note is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Note not found")
        return note

    async def replace(self, user: User, note_id: str, payload: NoteCreate) -> dict:
        note = await self.note_repo.replace_for_owner(note_id, user.id, payload)
        if note is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Note not found")
        return note

    async def delete(self, user: User, note_id: str) -> dict:
        deleted = await self.note_repo.delete_for_owner(note_id, user.id)
        if deleted is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Note not found")
        return deleted


NoteRepoDep = Annotated[NoteRepository, Depends(get_note_repository)]


def get_note_service(note_repo: NoteRepoDep) -> NoteService:
    return NoteService(note_repo)
