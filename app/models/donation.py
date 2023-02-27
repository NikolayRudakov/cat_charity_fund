# app/models/donation.py

from sqlalchemy import Column, Text, Integer, Boolean, DateTime, ForeignKey


from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
