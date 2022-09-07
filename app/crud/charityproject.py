from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


def project_lifetime(obj: CharityProject):
    print(1)
    if obj.close_date == 'null':
        print('close')
        return obj.close_date
    print('not close')
    return obj.create_date


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        query = select(
            [
                CharityProject.name,
                CharityProject.description,
                CharityProject.create_date,
                CharityProject.close_date,
            ]
        ).where(CharityProject.fully_invested)
        projects = await session.execute(query)
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
