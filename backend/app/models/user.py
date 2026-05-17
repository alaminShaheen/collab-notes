from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=20)
    full_name: str | None = Field(default=None, max_length=100)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
