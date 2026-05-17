from fastapi import Depends, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.user_repo import UserRepository, get_user_repository
from app.schemas import Token, UserCreate


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(self, payload: UserCreate) -> User:
        if self.user_repo.get_by_email(payload.email):
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
        if self.user_repo.get_by_username(payload.username):
            raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")

        user = User(
            email=payload.email,
            username=payload.username,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        return self.user_repo.create(user)

    def login(self, email_or_username: str, password: str) -> Token:
        user = (
            self.user_repo.get_by_email(email_or_username)
            or self.user_repo.get_by_username(email_or_username)
        )
        if not user or not user.id or not verify_password(password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        if not user.is_active:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is inactive")

        token = create_access_token(subject=user.id)
        return Token(access_token=token)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)
