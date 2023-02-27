# app/schemas/charity_project.py
from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, Extra, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectEdit(BaseModel):
    name: str = Field(None, max_length=100)
    description: str = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: datetime = Field(None)

    class Config:
        orm_mode = True
