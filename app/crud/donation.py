# app/crud/donatation.py
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    pass

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> List[Donation]:
        select_stmt = select(Donation).where(
            Donation.user_id == user.id,
        )
        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
