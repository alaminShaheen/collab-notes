from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.user import UserBase


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    full_name: str | None = None
    is_active: bool | None = None
