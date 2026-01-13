import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class GiveTiffinIn(BaseModel):
    person_id: uuid.UUID
    date: date


class UndoTiffinIn(BaseModel):
    person_id: uuid.UUID
    date: date


class TiffinLogOut(BaseModel):
    id: uuid.UUID
    person_id: uuid.UUID
    date: date
    action: str
    created_at: datetime


class PersonStatusOut(BaseModel):
    id: uuid.UUID
    name: str
    age: int
    given_count: int
    reversed_count: int
    total_tiffins: int


class TiffinStatusOut(BaseModel):
    date: date
    persons: list[PersonStatusOut]


class TiffinSummaryOut(BaseModel):
    month_name: str
    total_tiffins_this_month: int
    total_active_persons: int
    today_given: int
