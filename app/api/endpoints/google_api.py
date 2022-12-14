from typing import Any

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()

SPREADSHEETS_BASEURL = 'https://docs.google.com/spreadsheets/d/'


@router.get(
    '/',
    response_model=list[dict[str, Any]],
    dependencies=[Depends(current_superuser)],
)
async def get_spreadsheet(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    reservations = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    reservations,
                                    wrapper_services)
    spreadsheet_url = (
        SPREADSHEETS_BASEURL + spreadsheetid
    )
    return [
        {'spreadsheet_url': spreadsheet_url}
    ]
