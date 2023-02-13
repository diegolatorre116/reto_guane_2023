from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException

from app import internal, schemas
from app.internal.job_crud import job
from app.core.auth.role_checker import allow_clevel, allow_clevel_leader

jobs_router = APIRouter()

job_web_crud = internal.WebCRUDWrapper(
    internal.job,
    enty_name="job"
    )


@jobs_router.get(
    "/",
    response_model= list[schemas.Job],
    name="List all jobs"
)
async def get_jobs(current_user=Depends(allow_clevel_leader)) -> Any:
    """
    Get a list of all "job" entities. Allowed for "C-LEVEL" AND "LEADER"
    The return of the api has a following scheme:

    ```json
    [
    {
    "name": "Backend developer",
    "description": "backend managers",
    "id": 1,
    "department_id": 1
    },
    {
    "name": "Frontend developer",
    "description": "do frontend",
    "id": 2,
    "department_id": 1
    }
    ...
    ]
    ``` 
    """
    return await job_web_crud.get_all_entries()


@jobs_router.get(
    "/{job_id}",
    response_model= schemas.Job,
    name="Job info by id"
)
async def get_job_id(
    job_id:int,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Read one "job" entity based on its id. Allowed for "C-LEVEL" AND
    "LEADER"
    The return of the api has a following scheme:
    ```json
    {
    "name": "Backend developer",
    "description": "backend managers",
    "id": 1,
    "department_id": 1
    }
    ```
    """
    return await job_web_crud.get_enty_by_field("id", job_id)


@jobs_router.get(
    "/{job_id}/collaborators",
    response_model= list[schemas.Collaborator],
    name="List all collaborators of a job"
)
async def get_collaborators(job_id, current_user=Depends(allow_clevel_leader)):
    """
    Get a list of all "collaborators" entities that have a relationship
    with a "job" entitiy by job_id (FK).
    Allowed for "C-LEVEL" and "LEADER"
    The return of the api has a following scheme:
    ```json
    [
    {
        "name": "Diego",
        "last_name": "Latorre",
        "gender": "MALE",
        "age": 24,
        "is_active": true,
        "job_id": 1,
        "id": 1
    },
    {
        "name": "Andres",
        "last_name": "Alvarez",
        "gender": "MALE",
        "age": 25,
        "is_active": true,
        "job_id": 1,
        "id": 2
    }
    ...
    ]
    ```
    """
    try:
        collaborators = await job.get_collaborators_by_job(
            job_id
        )
    except Exception:
        raise HTTPException(
            500,
            detail="Failed to get collaborators. The job probably does"
            " not exist in the database."
        )

    if len(collaborators) == 0:
        raise HTTPException(
            400,
            detail="No collaborators found."
        )

    return collaborators


@jobs_router.post(
    "/",
    response_model=schemas.Job,
    name="Create new job",
    status_code=status.HTTP_201_CREATED
)
async def create_job(
    job_in: schemas.JobCreate,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Create one "job" entity. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Frontend developer",
    "description": "Frontend managers",
    "id": 2,
    "department_id": 1
    }
    ```
    """
    return await job_web_crud.post_enty(
        enty_info=job_in
    )


@jobs_router.patch(
    "/{job_id}",
    response_model = schemas.Job,
    name="Update job by id"
)
async def update_job_by_name(
    job_id:int,
    job_update:schemas.JobUpdate,
    current_user=Depends(allow_clevel)
):
    """
    Update one "job" entity by id. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": null,
    "description": "do frontend",
    "id": null,
    "department_id": null
    }
    ```
    (In this example only the description was updated)
    """
    return await job_web_crud.update_enty_by_field(
        field="id",
        value_in=job_id,
        enty_new_info=job_update
    )
    

@jobs_router.delete(
    "/{job_id}",
    response_model = schemas.Job,
    name="Delete job by id"
)
async def delete_job_by_name(
    job_id:int,
    current_user=Depends(allow_clevel)
):
    """
    Delete one "job" entity bases on its id.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Frontend developer",
    "description": "Frontend managers",
    "id": 2,
    "department_id": 1
    }
    ```
    """
    return await job_web_crud.delete_enty_by_field(
        field="id",
        value_in=job_id
    )