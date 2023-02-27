# app/services/invest.py
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


async def process_invest(session: AsyncSession):

    open_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0)
    )
    open_projects_all = open_projects.scalars().all()

    total_need = 0
    for project in open_projects_all:
        total_need = total_need + project.full_amount - project.invested_amount

    open_donations = await session.execute(
        select(Donation).where(Donation.fully_invested == 0)
    )
    open_donations = open_donations.scalars().all()

    total_have = 0
    for donation in open_donations:
        total_have = total_have + donation.full_amount - donation.invested_amount

    if total_have < total_need:
        total = total_have
        total_d = total_have
    else:
        total = total_need
        total_d = total_need

    while total > 0:
        open_project = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0)
        )
        open_project = open_project.scalars().first()
        project_sum = open_project.full_amount - open_project.invested_amount
        if project_sum <= total:
            total = total - project_sum
            setattr(open_project, "invested_amount", open_project.full_amount)
            setattr(open_project, "fully_invested", True)
            setattr(open_project, "close_date", datetime.now())
            session.add(open_project)
        else:
            setattr(
                open_project, "invested_amount", open_project.invested_amount + total
            )
            total = 0
            session.add(open_project)

    while total_d > 0:
        open_donation = await session.execute(
            select(Donation).where(Donation.fully_invested == 0)
        )
        open_donation = open_donation.scalars().first()
        donation_sum = open_donation.full_amount - open_donation.invested_amount
        if donation_sum <= total_d:
            total_d = total_d - donation_sum
            setattr(open_donation, "invested_amount", open_donation.full_amount)
            setattr(open_donation, "fully_invested", True)
            setattr(open_donation, "close_date", datetime.now())
            session.add(open_donation)
        else:
            setattr(
                open_donation,
                "invested_amount",
                open_donation.invested_amount + total_d,
            )
            total_d = 0
            session.add(open_donation)

    await session.commit()
    await session.execute(select(Donation))
    await session.execute(select(CharityProject))
    # await session.refresh() не работает
