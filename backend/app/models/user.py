from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

# Base class with shared fields
class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)
    full_name: str | None = Field(default=None, max_length=100)
    is_active: bool = True


# Table model
class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserRead(UserBase):
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    full_name: str | None = None
    is_active: bool | None = None