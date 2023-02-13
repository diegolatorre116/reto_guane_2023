from typing import Any
from datetime import date

from fastapi import APIRouter, HTTPException, Depends

from app import internal, schemas
from app.internal.announcement_crud import announcement
from app.core.auth.role_checker import allow_clevel

announcements_router = APIRouter()


@announcements_router.get(
    "/today",
    response_model= list[schemas.Announcement],
    name="Get all the announcements from today"
)
async def announcements_today(current_user=Depends(allow_clevel)) -> Any:
    """
    Get all "announcement" entities created today.
    Allowed for "C-LEVEL"
    """
    announcements = await announcement.today_announcement()
    if len(announcements) != 0:
            return announcements
    else:
        raise HTTPException(
                400,
                detail=f"No announcements found"
            )
            

@announcements_router.get(
    "/{start_date}/{final_date}}",
    response_model= list[schemas.Announcement],
    name="Get announcements between dates"
)
async def announcements_today(
    start_date:date,
    final_date:date,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Get all "announcement" entities created in the range
    between start_date and final_date.
    Allowed for "C-LEVEL"
    """
    announcements = await announcement.announcements_between_dates(
        start_date,
        final_date
    )
    if len(announcements) != 0:
            return announcements
    else:
        raise HTTPException(
                400,
                detail=f"No announcements found"
            )