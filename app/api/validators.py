from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectDB, CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await (
        charity_project_crud.get_charity_project_id_by_name(
            project_name, session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_greater_than_invested_funds(
        new_value: int,
        charity_project: CharityProject,
) -> CharityProject:
    if charity_project.invested_amount > new_value:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Новая сумма инвестирования '
                   'меньше чем внесенные средства'
        )
    return charity_project


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return charity_project


async def check_project_update_is_possible(
        old_obj: CharityProjectDB,
        new_data: CharityProjectUpdate,
        session: AsyncSession,
) -> None:
    if not (new_data.name or new_data.description or new_data.full_amount):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Необходимо ввести новые данные',
        )
    if new_data.name:
        await check_name_duplicate(
            new_data.name, session
        )
    if new_data.description == '':
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Описание не должно быть пустым',
        )
    if new_data.full_amount:
        await check_greater_than_invested_funds(
            new_data.full_amount, old_obj
        )
    if old_obj.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
