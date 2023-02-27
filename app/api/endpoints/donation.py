# app/api/endpoints/donation.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB
from app.services.invest import process_invest

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude={
        "fully_invested",
        "invested_amount",
        "user_id",
    },
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Инвестируйте тут"""

    new_donation = await donation_crud.create(donation, session, user)
    await process_invest(session)

    return new_donation


@router.get(
    "/",
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    "/my",
    response_model=List[DonationDB],
    response_model_exclude={"fully_invested", "invested_amount", "user_id"},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
