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
    * "start_filter": Start date to filter assignments
    * "final_filter": Final date to filter assignments
    :return: List of assignments that are valid during the date
    range between the start_date and final_date parameters.
    Assignments will be grouped by project, by job, and by
    collaborator. For each job, the "start_date" and "final_date"
    correspond to the earliest and latest date for some assignment
    associated with the job. This is to be able to show in a calendar
    view the usage of each job.
    The return of the api has a following scheme:
    ```json
    [
        {
        "project_id": 1,
        "project_name": "Project rock",
        "jobs_implicated": [
        {
            "start_date": "2023-02-10",
            "end_date": "2023-02-25",
            "job_id": 1,
            "job_name": "Backend",
            "collaborators": [
            {
                "id": 1,
                "name": "Elias",
                "lastname": "quintero",
                "assignments": [
                {
                    "project_id": 1,
                    "collaborator_id": 1,
                    "id": 1,
                    "start_date": "2023-02-10",
                    "final_date": "2023-02-20",
                    "name": "tarea de backend"
                },
                {
                    "project_id": 1,
                    "collaborator_id": 1,
                    "id": 9,
                    "start_date": "2023-03-11",
                    "final_date": "2023-03-17",
                    "name": "Tarea de backend"
                }
                ]
            },
            {
                "id": 2,
                "name": "Diego",
                "lastname": "latorre",
                "assignments": [
                {
                    "project_id": 1,
                    "collaborator_id": 2,
                    "id": 2,
                    "start_date": "2023-02-10",
                    "final_date": "2023-02-25",
                    "name": "tarea de backend"
                ]
            }
            ]
        }
        ]
    }, ... 
    ]
    ```
    """
    return await assignment_calendar.calendar(
        start_filter,
        final_filter
    )


