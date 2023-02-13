from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException

from app import internal, schemas
from app.internal.assignment_crud import assignment
from app.core.auth.role_checker import allow_clevel_leader


assignments_router = APIRouter()

assignment_web_crud = internal.WebCRUDWrapper(
    assignment,
    enty_name="assignment"
)


@assignments_router.get(
    "/",
    response_model= list[schemas.Assignment],
    name="List all assignments"
)
async def get_assignments(current_user=Depends(allow_clevel_leader)) -> Any:
    """
    Get a list of all "assignment" entities. Allowed for "C-LEVEL" AND 
    "LEADER".
    Allowed for "C-LEVEL" AND "LEADER"
    """
    return await assignment_web_crud.get_all_entries()


@assignments_router.get(
    "/{assignment_id}",
    response_model= schemas.Assignment,
    name="Assignment info by id"
)
async def get_job_id(
    assignment_id:int,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Read one "assignmment" entity based on its id.
    Allowed for "C-LEVEL" and "LEADER".
    """
    return await assignment_web_crud.get_enty_by_field("id", assignment_id)


@assignments_router.post(
    "/",
    response_model=schemas.Assignment,
    status_code=status.HTTP_201_CREATED
)
async def create_assignment(
    assignment_in: schemas.AssignmentCreate,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Create one "assignment" entity. In order to create the "assignment",
    the collaborator must be added to the corresponding project.
    Allowed for "C-LEVEL" and "LEADER".
    """
    try:
        create_assignment = await assignment.create(
            assignment_in
        )
    except internal.CollaboratorNotInProject:
        raise HTTPException(
            500,
            detail="The collaborator is not assigned to the project"
        )
    except Exception as e:
        raise HTTPException(
            500,
            detail="Error while creating assignation in database"
        )

    if not create_assignment:
        raise HTTPException(
                400,
                detail=f'Create query of new assignment finished'  
                    ' but was not saves'
            )

    return create_assignment


@assignments_router.patch(
    "/{assignment_id}",
    response_model = schemas.Assignment,
    name="Update assignment by id"
)
async def update_assignment_by_id(
    assignment_id:int,
    assignment_update:schemas.AssignmentUpdate,
    current_user=Depends(allow_clevel_leader)
):
    """
    Update one "assignment" entity by id. Allowed for "C-LEVEL" and
    "LEADER"
    """
    return await assignment_web_crud.update_enty_by_field(
        field="id",
        value_in=assignment_id,
        enty_new_info=assignment_update
    )
    

@assignments_router.delete(
    "/{assignment_id}",
    response_model = schemas.Assignment,
    name="Delete assignment by id"
)
async def delete_assignment_by_id(
    assignment_id:int,
    current_user=Depends(allow_clevel_leader)
):
    """
    Delete one "assignment" entity bases on its id.
    Allowed for "C-LEVEL" and "LEADER".
    """
    return await assignment_web_crud.delete_enty_by_field(
        field="id",
        value_in=assignment_id
    )