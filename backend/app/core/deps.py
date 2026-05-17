from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.security import JWTError, decode_access_token
from app.models import User
from app.repositories.user_repo import UserRepository, get_user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_current_user(token: TokenDep, user_repo: UserRepoDep) -> User:
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError, InvalidTokenError):
        raise creds_exc

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise creds_exc
    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]