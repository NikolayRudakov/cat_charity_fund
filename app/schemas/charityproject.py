# app/schemas/charity_project.py
from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, Extra, PositiveInt


class CharityProjectBase(BaseModel, extra=Extra.forbid):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectEdit(BaseModel, extra=Extra.forbid):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True
