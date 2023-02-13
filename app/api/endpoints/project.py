from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException

from app import internal, schemas
from app.internal import project, project_collaborator_obj, announcement
from app.core.auth.role_checker import allow_clevel, allow_clevel_leader
from app.internal.handler_announcement import InfoCollaboratorAnnouncement

projects_router = APIRouter()

project_web_crud = internal.WebCRUDWrapper(
    internal.project,
    enty_name="project"
    )


@projects_router.get(
    "/",
    response_model= list[schemas.Project],
    name="List all projects"
)
async def get_projects(current_user=Depends(allow_clevel_leader)) -> Any:
    """
    Get a list of all "projects" entities. Allowed for "C-LEVEL" AND
    "LEADER"
    The return of the api has a following scheme:

    ```json
    [
    {
        "name": "Avigail",
        "description": "About avigail",
        "customer": "Apple",
        "start_date": "2023-02-13",
        "final_date": "2023-11-13",
        "id": 1
    },
    {
        "name": "Addam",
        "description": "About addam",
        "customer": "Microsoft",
        "start_date": "2023-02-13",
        "final_date": "2023-12-15",
        "id": 2
    }...
    ]
    ``` 
    """
    return await project_web_crud.get_all_entries()


@projects_router.get(
    "/count",
    name="Count all projects"
)
async def count_projects(current_user=Depends(allow_clevel)) -> Any:
    """
    Get the total number of "project" entity records.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    2
    ```
    """
    return await internal.project.count_records()


@projects_router.get(
    "/{project_id}/collaborators",
    response_model=list[schemas.Collaborator],
    name="List all collaborators of a project"
)
async def collaborators_in_project(
    project_id:int,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Get a list of all "collaborator" entities that have a relationship 
    with a "project" entitiy by project_id (FK).
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
    ]
    ```
    """
    try:
        collaborators = await project.get_collaborators_by_project(
            project_id
        )
    except Exception:
        raise HTTPException(
            500,
            detail="Failed to get collaborators. The project probably does"
            " not exist in the database."
        )
    
    if len(collaborators) == 0:
        raise HTTPException(
            400,
            detail="No collaborators found."
        )

    return collaborators


@projects_router.get(
    "/{project_id}/assignments",
    response_model= list[schemas.Assignment],
    name="List all assignments of a project"
)
async def get_assignments(
    project_id, 
    current_user=Depends(allow_clevel_leader)
    ):
    """
    Get a list of all "assignment" entities that have a relationship with
    a "project" entitiy by project_id (FK).
    Allowed for "C-LEVEL" and "LEADER"
    The return of the api has a following scheme:
    ```json
    [
    {
        "name": "task1",
        "start_date": "2023-02-13",
        "final_date": "2023-02-20",
        "id": 1,
        "collaborator_id": 1,
        "project_id": 1
    },
    {
        "name": "task2",
        "start_date": "2023-02-22",
        "final_date": "2023-02-27",
        "id": 2,
        "collaborator_id": 1,
        "project_id": 1
    }...
    ]
    ```
    """
    try:
        assignments =  await project.get_asignments_by_project(
            project_id
        )
    except Exception:
        raise HTTPException(
            500,
            detail="Failed to get assignments. The project probably does"
            " not exist in the database."
        )

    if len(assignments) == 0:
        raise HTTPException(
            400,
            detail="No assignments found."
        )

    return assignments


@projects_router.get(
    "/{project_id}",
    response_model= schemas.Project,
    name="Project info by id"
)
async def get_project_by_id(
    project_id:int,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Read one "project" entity based on its id. Allowed for "C-LEVEL" AND
    "LEADER"
    The return of the api has a following scheme:
    ```json
    {
    "name": "Avigail",
    "description": "About avigail",
    "customer": "Apple",
    "start_date": "2023-02-13",
    "final_date": "2023-11-13",
    "id": 1
    }
    ```
    """
    return await project_web_crud.get_enty_by_field("id", project_id)


@projects_router.post(
    "/",
    response_model=schemas.Project,
    status_code=status.HTTP_201_CREATED
)
async def create_project(
    project_in: schemas.ProjectCreate,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Create one "project" entity. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Avigail",
    "description": "About avigail",
    "customer": "Apple",
    "start_date": "2023-02-13",
    "final_date": "2023-11-13",
    "id": 1
    }
    ```
    """
    return await project_web_crud.post_enty(
        enty_info=project_in
    )


@projects_router.post(
    "/{project_id}/add/{collaborator_id}",
    #response_model=schemas.,
    name="add collaborator to project",
    status_code=status.HTTP_201_CREATED
)
async def add_collaborator(
    project_id,
    collaborator_id,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Add collaborator to project. A collaborator can only be assigned
    once to a project, otherwise an HTTP exception 500 will be thrown.
    After adding the collaborator, an announcement will be created with
    this information.
    Allowed for "C-LEVEL"
    The return of the api has a following scheme:
    ```json
    {
    "collaborator_id": 2,
    "id": 2,
    "project_id": 1
    }
    ```
    """
    try:
        new_collaborator = await project_collaborator_obj.add_collaborator(
        project_id,
        collaborator_id
    )
    except Exception:
        raise HTTPException(
            500,
            detail="Error while adding collaborator to project. The"
            " collaborator may already be added to the project."
        )

    if not new_collaborator:
        raise HTTPException(
            400,
            detail="Create query of new collaborator finished but was"
            " not save"
        )
    
    try: 
        await announcement.create_announcement(
            obj_in={
                "name": await InfoCollaboratorAnnouncement.create_name(),
                "description": await InfoCollaboratorAnnouncement.create_description
                (
                current_user,
                project_id, 
                collaborator_id,
                "eliminated"
                ),
                "user_id": current_user["id"]   
            }
        )
    except Exception:
        return "The collaborator was added to the project but the"\
        " corresponding announcement could not be created."

    return new_collaborator


@projects_router.patch(
    "/{project_id}",
    response_model = schemas.Project,
    name="Update project by id"
)
async def update_project_by_id(
    project_id:int,
    project_update:schemas.ProjectUpdate,
    current_user=Depends(allow_clevel)
):
    """
    Update one "project" entity by id. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": null,
    "description": null,
    "customer": null,
    "start_date": "2023-02-13",
    "final_date": null,
    "id": null
    }
    (In this example only the start_date was updated)
    ```
    """
    return await project_web_crud.update_enty_by_field(
        field="id",
        value_in=project_id,
        enty_new_info=project_update
    )
    

@projects_router.delete(
    "/{project_id}",
    response_model = schemas.Project,
    name="Delete project by id"
)
async def delete_project_by_id(
    project_id:int,
    current_user=Depends(allow_clevel)
):
    """
    Delete one "project" entity bases on its id.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Avigail",
    "description": "About avigail",
    "customer": "Apple",
    "start_date": "2023-02-13",
    "final_date": "2023-11-13",
    "id": 1
    }
    ```
    """
    return await project_web_crud.delete_enty_by_field(
        field="id",
        value_in=project_id
    )


@projects_router.delete(
    "/remove/{project_id}/{colllaborator_id}",
    #response_model = schemas.
    name="Remove collaborator to project"
)
async def delete_collaborator_to_project(
    project_id:int,
    collaborator_id:int,
    current_user=Depends(allow_clevel)
):
    """
    Remove collaborator to project by project_id and collaborator_id.
    After removin the collaborator, an announcement will be created with
    this information.
    Allowed for "C-LEVEL"
    The return of the api has a following scheme:
    ```json
    {
    "collaborator_id": 2,
    "id": 2,
    "project_id": 1
    }
    ```
    """
    try:
        collaborator_delete = await project_collaborator_obj.remove_collaborator(
            project_id,
            collaborator_id
        )
    except Exception:
        raise HTTPException(
            500,
            detail="It is possible that the collaborator does not belong"
            " to the project or that the project/collaborator does not" 
            " exist in the database"
        )

    if not collaborator_delete:
            raise HTTPException(
                400,
                detail="The collaborator could not be removed from the project"
            )
    
    try: 
        await announcement.create_announcement(
            obj_in={
                "name": await InfoCollaboratorAnnouncement.create_name(),
                "description": await InfoCollaboratorAnnouncement.create_description
                (
                current_user,
                project_id, 
                collaborator_id,
                "eliminated"
                ),
                "user_id": current_user["id"]    
            }
        )
    except Exception:
        return "The collaborator was added to the project but the"\
        " corresponding announcement could not be created."
    
    return collaborator_delete