import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PersonCreateIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    age: int = Field(ge=0, le=150)


class PersonOut(BaseModel):
    id: uuid.UUID
    name: str
    age: int
    created_at: datetime
