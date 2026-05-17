from datetime import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Response body returned by /auth/login."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """The decoded contents of a JWT. Used internally for validation."""
    sub: str
    exp: datetime
    iat: datetime | None = None


class LoginRequest(BaseModel):
    """JSON body for /auth/login (skip if using OAuth2PasswordRequestForm)."""
    email: EmailStr
    password: str
