from typing import Any

from fastapi import APIRouter, status, Depends

from app import internal, schemas

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
async def get_jobs() -> Any:
    """
    Get all jobs.
    """
    return await job_web_crud.get_all_entries()


@jobs_router.get(
    "/{name}",
    response_model= schemas.Job,
    name="Job info by name"
)
async def get_job_by_name(name:str) -> Any:
    """
    Get a specific job by name.
    """
    return await job_web_crud.get_enty_by_field("name", name)


@jobs_router.post(
    "/",
    response_model=schemas.Job,
    status_code=status.HTTP_201_CREATED
)
async def create_job(job_in: schemas.JobCreate) -> Any:
    """
    Create new job
    """
    return await job_web_crud.post_enty(
        enty_info=job_in
    )


@jobs_router.patch(
    "/{name}",
    response_model = schemas.Job,
    name="Update job by name"
)
async def update_job_by_name(
    name:str,
    job_update:schemas.JobUpdate
):
    """
    Update job by name
    """
    return await job_web_crud.update_enty_by_field(
        field="name",
        value_in=name,
        enty_new_info=job_update
    )
    

@jobs_router.delete(
    "/{name}",
    response_model = schemas.Job,
    name="Delete job by name"
)
async def delete_job_by_name(
    name:str,
):
    """
    Delete job by name
    """
    return await job_web_crud.delete_enty_by_field(
        field="name",
        value_in=name
    )