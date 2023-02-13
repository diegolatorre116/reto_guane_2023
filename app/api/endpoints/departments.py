from typing import Any

from fastapi import APIRouter, status, Depends

from app import internal, schemas
from app.core.auth.role_checker import allow_clevel, allow_clevel_leader

departments_router = APIRouter()

department_web_crud = internal.WebCRUDWrapper(
    internal.deparment,
    enty_name="deparment"
    )


@departments_router.get(
    "/",
    response_model= list[schemas.Department],
    name="List all departments"
)
async def get_deparments(current_user=Depends(allow_clevel)) -> Any:
    """
    Get a list of all "department" entities. Allowed for "C-LEVEL".
    The return of the api has a following scheme:

    ```json
    [
    {
        "name": "Development",
        "description": "Software_Development",
        "id": 1
    },
    {
        "name": "Data Science",
        "description": "Data science department",
        "id": 2
    }
    ...
    ]
    ``` 
    """
    return await department_web_crud.get_all_entries()


@departments_router.get(
    "/count",
    name="Count all departments"
)
async def count_deparments(current_user=Depends(allow_clevel)) -> Any:
    """
    Get the total number of "department" entity records.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    2
    ```
    """
    return await internal.deparment.count_records()


@departments_router.get(
    "/{department_id}",
    response_model= schemas.Department,
    name="Deparment info by id"
)
async def get_department_id(
    department_id:int,
    current_user=Depends(allow_clevel_leader)
    ) -> Any:
    """
    Read one "department" entity based on its id.
    Allowed for "C-LEVEL" AND "LEADER".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Development",
    "description": "Software_Development",
    "id": 1
    }
    ```
    """
    return await department_web_crud.get_enty_by_field("id", department_id)


@departments_router.post(
    "/",
    response_model=schemas.Department,
    name="Create new department",
    status_code=status.HTTP_201_CREATED
)
async def create_department(
    deparment_in: schemas.DepartmentCreate,
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Create one "department" entity.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Development",
    "description": "Software_Development",
    "id": 1
    }
    ```
    """
    return await department_web_crud.post_enty(
        enty_info=deparment_in
    )


@departments_router.patch(
    "/{department_id}",
    response_model = schemas.Department,
    name="Update department by id"
)
async def update_deparment_id(
    department_id:int,
    department_update:schemas.DepartmentUpdate,
    current_user=Depends(allow_clevel)
):
    """
    Update one "department" entity by id.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": null,
    "description": "Revamped data science department",
    "id": null
    }
    ```
    (In this example only the description was updated)
    """
    return await department_web_crud.update_enty_by_field(
        field="id",
        value_in=department_id,
        enty_new_info=department_update
    )
    

@departments_router.delete(
    "/{department_id}",
    response_model = schemas.Department,
    name="Delete deparment by id"
)
async def delete_deparment_id(
    department_id:int,
    current_user=Depends(allow_clevel)
):
    """
    Delete one "deparment" entity bases on its id.
    Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "name": "Development",
    "description": "Software_Development",
    "id": 1
    }
    ```
    """
    return await department_web_crud.delete_enty_by_field(
        field="id",
        value_in=department_id
    )



    