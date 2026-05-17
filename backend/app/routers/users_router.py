from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import CurrentUser
from app.repositories.user_repo import UserRepository, get_user_repository
from app.schemas import NoteRead, UserRead
from app.services.note_service import NoteService, get_note_service

router = APIRouter(prefix="/users", tags=["users"])

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]


@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUser):
    return current_user


@router.get("/{user_id}/notes", response_model=list[NoteRead])
async def list_user_notes(
    user_id: int,
    current_user: CurrentUser,
    user_repo: UserRepoDep,
    note_service: NoteServiceDep,
):
    target = user_repo.get_by_id(user_id)
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return await note_service.list_for_user(target)
