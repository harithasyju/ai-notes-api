from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    summary: str | None = None
    class Config:
        from_attributes = True

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)