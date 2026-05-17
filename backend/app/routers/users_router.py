from fastapi import APIRouter

from app.core.deps import CurrentUser
from app.schemas import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUser):
    return current_user