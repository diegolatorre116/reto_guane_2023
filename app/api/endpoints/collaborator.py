from typing import Any
from datetime import date

from fastapi import APIRouter, status, Depends, HTTPException

from app import internal, schemas
from app.internal.collaborator_crud import collaborator
from app.core.auth.role_checker import allow_clevel, allow_clevel_leader

collaborators_router = APIRouter()

collaborator_web_crud = internal.WebCRUDWrapper(
    internal.collaborator,
    enty_name="collaborator"
    )


@collaborators_router.get(
    "/",
    response_model= list[schemas.Collaborator],
    name="List all collaborators"
)
async def get_collaborators(current_user=Depends(allow_clevel_leader)) -> Any:
    """
    Get a list of all "collaborator" entities. Allowed for "C-LEVEL"
    and "LEADER"
    """
    return await collaborator_web_crud.get_all_entries()


@collaborators_router.get(
    "/count",
    name="Count all collaborators"
)
async def count_collaborators(current_user=Depends(allow_clevel)) -> Any:
    """
    Get the total number of "collaborator" entity records.
    Allowed for "C-LEVEL".
    """
    return await collaborator.count_records()


@collaborators_router.get(
    "/count_actives",
    name="Count active collaborators"
)
async def count_active_collaborators(current_user=Depends(allow_clevel)) -> Any:
    """
    Count all "collaborators" entities that are active (is_active=True).
    A collaborator may not be active due to permission, disability, etc..
    Allowed for "C-LEVEL"
    """
    return await collaborator.count_by_field(
        field="is_active",
        value=True
    )


@collaborators_router.get(
    "/count/{job_id}",
    name="Count collaborators by job_id"
)
async def count_collaborators_job(
    job_id,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Count "collaborator" entities by "job_id". This endpoint fulfills the
    functionality of knowing things like: How many backend dev do
    we have?, How many data science do we have? etc
    Allowed for "C-LEVEL"
    """
    return await collaborator.count_by_field(
        field="job_id",
        value=job_id
    )


@collaborators_router.get(
    "/{collaborator_id}",
    response_model= schemas.Collaborator,
    name="Collaborator info by id"
)
async def get_collaborator_by_id(
    collaborator_id:int,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Read one "collaborator" entity based on its id. Allowed for
    "C-LEVEL" AND "LEADER"
    """
    return await collaborator_web_crud.get_enty_by_field("id", collaborator_id)


@collaborators_router.get(
    "/{collaborator_id}/assignments",
    response_model= list[schemas.Assignment],
    name="List all assignments of a collaborator"
)
async def get_assignments(
    collaborator_id,
    current_user=Depends(allow_clevel_leader)
    ):
    """
    Get a list of all "assignments" entities that have a relationship
    with a "collaborator" entitiy by collaborator_id (FK).
    Allowed for "C-LEVEL" AND "LEADER".
    """
    try:
        assignments =  await collaborator.get_assignments_by_collaborator(
            collaborator_id
        )
    except Exception:
        raise HTTPException(
            500,
            detail="Failed to get assignments. The collaborator probably does"
            " not exist in the database."
        )

    if len(assignments) == 0:
        raise HTTPException(
            400,
            detail="No assignments found."
        )

    return assignments


@collaborators_router.post(
    "/",
    response_model=schemas.Collaborator,
    name="Create new collaborator",
    status_code=status.HTTP_201_CREATED
)
async def create_collaborator(
    collaborator_in: schemas.CollaboratorCreate,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Create one "collaborator" entity. There are two possible genders:
    "MALE" and "FEMALE". Allowed for "C-LEVEL"
    """
    return await collaborator_web_crud.post_enty(
        enty_info=collaborator_in
    )


@collaborators_router.patch(
    "/{collaborator_id}",
    response_model = schemas.Collaborator,
    name="Update collaborator by id"
)
async def update_collaborator_by_id(
    collaborator_id:int,
    collaborator_update:schemas.CollaboratorUpdate,
    current_user=Depends(allow_clevel)
):
    """
    Update one "collaborator" entity by id. Allowed for "C-LEVEL".
    """
    return await collaborator_web_crud.update_enty_by_field(
        field="id",
        value_in=collaborator_id,
        enty_new_info=collaborator_update
    )
    

@collaborators_router.delete(
    "/{collaborator_id}",
    response_model = schemas.Collaborator,
    name="Delete collaborator by id"
)
async def delete_collaborator_by_id(
    collaborator_id:int,
    current_user=Depends(allow_clevel)
):
    """
    Delete one "collaborator" entity bases on its id.
    Allowed for "C-LEVEL".
    """
    return await collaborator_web_crud.delete_enty_by_field(
        field="id",
        value_in=collaborator_id
    )


@collaborators_router.get(
    "/available/{job_id}/{date}",
    response_model = list[schemas.Collaborator],
    name="List all collaborators available for a specific day"
)
async def available_collaborators(
    job_id: int,
    date: date,
    current_user=Depends(allow_clevel)
):
    """
    asd
    """
    return await collaborator.filter_availability(
        date=date,
        job_id=job_id
    )