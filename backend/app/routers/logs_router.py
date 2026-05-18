from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import CurrentUser
from app.schemas import LogRead
from app.services.log_service import LogService, get_log_service

router = APIRouter(prefix="/logs", tags=["logs"])

LogServiceDep = Annotated[LogService, Depends(get_log_service)]


@router.get("", response_model=list[LogRead])
async def list_logs(
    user: CurrentUser,
    log_service: LogServiceDep,
    user_id: Annotated[int | None, Query()] = None,
    event_type: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    skip: Annotated[int, Query(ge=0)] = 0,
):
    return await log_service.list(user_id, event_type, limit, skip)
