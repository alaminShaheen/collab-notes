from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="", max_length=100_000)
    tags: List[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
