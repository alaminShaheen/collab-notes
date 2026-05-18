from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.deps import CurrentUser
from app.schemas import SearchResult
from app.schemas.note import NoteCreate, NoteRead
from app.services.log_service import LogService, get_log_service
from app.services.note_service import NoteService, get_note_service
from app.services.search_service import SearchService, get_search_service

router = APIRouter(prefix="/notes", tags=["notes"])

NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]
LogServiceDep = Annotated[LogService, Depends(get_log_service)]
SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate,
    user: CurrentUser,
    service: NoteServiceDep,
    log_service: LogServiceDep,
    search_service: SearchServiceDep,
):
    note = await service.create(user, payload)
    await search_service.index_note(note)
    await log_service.note_created(user.id, note["id"], note["title"])
    return note


@router.get("", response_model=list[NoteRead])
async def list_notes(user: CurrentUser, service: NoteServiceDep):
    return await service.list_for_user(user)


@router.get("/search", response_model=list[SearchResult])
async def search_notes(
    user: CurrentUser,
    search_service: SearchServiceDep,
    log_service: LogServiceDep,
    q: Annotated[str, Query(min_length=1)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    skip: Annotated[int, Query(ge=0)] = 0,
):
    results = await search_service.search_notes(q, limit, skip)
    await log_service.note_searched(user.id, q)
    return results


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: str, user: CurrentUser, service: NoteServiceDep):
    return await service.get(user, note_id)


@router.put("/{note_id}", response_model=NoteRead)
async def replace_note(
    note_id: str,
    payload: NoteCreate,
    user: CurrentUser,
    service: NoteServiceDep,
    log_service: LogServiceDep,
    search_service: SearchServiceDep,
):
    note = await service.replace(user, note_id, payload)
    await search_service.index_note(note)
    await log_service.note_updated(
        user.id, note["id"], list(payload.model_dump().keys())
    )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    user: CurrentUser,
    service: NoteServiceDep,
    log_service: LogServiceDep,
    search_service: SearchServiceDep,
):
    deleted = await service.delete(user, note_id)
    await search_service.delete_note(deleted["id"])
    if not user.id:
        return
    await log_service.note_deleted(user.id, deleted["id"], deleted["title"])
