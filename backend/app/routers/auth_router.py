from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Token, UserCreate, UserRead
from app.services.auth_service import AuthService, get_auth_service
from app.services.log_service import LogService, get_log_service

router = APIRouter(prefix="/auth", tags=["auth"])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
LogServiceDep = Annotated[LogService, Depends(get_log_service)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate, auth_service: AuthServiceDep, log_service: LogServiceDep):
    user = auth_service.signup(payload)
    await log_service.user_signup(user.id, user.username)
    return user


@router.post("/login", response_model=Token)
async def login(form: OAuth2FormDep, auth_service: AuthServiceDep, log_service: LogServiceDep):
    user, token = auth_service.login(email_or_username=form.username, password=form.password)
    await log_service.user_login(user.id, user.username)
    return token
