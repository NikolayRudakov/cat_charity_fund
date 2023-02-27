# app/api/endpoints/charity_project.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_if_can_delite_project,
    check_if_can_edit_project,
)
from typing import List
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.invest import process_invest
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectEdit,
)


router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await process_invest(session)
    return new_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude={"close_data"},
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):

    projects = await charity_project_crud.get_multi(session)
    return projects


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delite_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_if_can_delite_project(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectEdit,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_if_can_edit_project(project_id, obj_in.full_amount, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await charity_project_crud.update(project, obj_in, session)
    await process_invest(session)
    return project
