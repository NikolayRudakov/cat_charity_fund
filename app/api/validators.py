# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def check_if_can_delite_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(obj_id=project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    if project.invested_amount > 0 or project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )

    return project


async def check_if_can_edit_project(
    project_id: int,
    new_full_amount: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(obj_id=project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="Закрытый проект нельзя редактировать!",
        )
    if new_full_amount:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail="Нельзя установить требуемую сумму меньше уже вложенной.",
            )

    return project
