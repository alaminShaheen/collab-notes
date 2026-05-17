from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Token, UserCreate, UserRead
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, auth_service: AuthServiceDep):
    return auth_service.signup(payload)


@router.post("/login", response_model=Token)
def login(form: OAuth2FormDep, auth_service: AuthServiceDep):
    return auth_service.login(email_or_username=form.username, password=form.password)