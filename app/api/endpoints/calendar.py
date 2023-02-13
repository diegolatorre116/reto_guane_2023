from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException

from app import internal, schemas
from app.internal.calendar import assignment_calendar
from app.core.auth.role_checker import allow_clevel


calendar_router = APIRouter()


@calendar_router.get(
    "/{start_filter}/{final_filter}",
    name="Calendar"
)
async def calendar(
    start_filter, 
    final_filter,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    blablablas
    """
    return await assignment_calendar.calendar(
        start_filter,
        final_filter
    )


