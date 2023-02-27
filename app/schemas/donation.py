# app/schemas/donation.py
from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationCreate):
    id: int
    create_date: datetime = Field(datetime.now())
    fully_invested: bool
    invested_amount: Optional[int]
    user_id: int

    class Config:
        orm_mode = True
