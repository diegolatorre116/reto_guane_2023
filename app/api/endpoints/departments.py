from typing import Any

from fastapi import APIRouter, status, Depends

from app import internal, schemas

departments_router = APIRouter()

deparment_web_crud = internal.WebCRUDWrapper(
    internal.deparment,
    enty_name="deparment"
    )


@departments_router.get(
    "/",
    response_model= list[schemas.Department],
    name="List all departments"
)
async def get_deparments() -> Any:
    """
    Get all deparments.
    """
    return await deparment_web_crud.get_all_entries()


@departments_router.get(
    "/count",
    name="Count all departments"
)
async def get_deparments() -> Any:
    """
    Get the total number of departments created.
    """
    return await internal.deparment.count_departments()



@departments_router.get(
    "/{name}",
    response_model= schemas.Department,
    name="Deparment info by name"
)
async def get_deparment_by_name(name:str) -> Any:
    """
    Get a specific deparment by name.
    """
    return await deparment_web_crud.get_enty_by_field("name", name)


@departments_router.post(
    "/",
    response_model=schemas.Department,
    status_code=status.HTTP_201_CREATED
)
async def create_department(deparment_in: schemas.DepartmentCreate) -> Any:
    """
    Create new department
    """
    return await deparment_web_crud.post_enty(
        enty_info=deparment_in
    )


@departments_router.patch(
    "/{name}",
    response_model = schemas.Department,
    name="Update deparment by name"
)
async def update_deparment_by_name(
    name:str,
    department_update:schemas.DepartmentUpdate
):
    """
    Update deparment by name
    """
    return await deparment_web_crud.update_enty_by_field(
        field="name",
        value_in=name,
        enty_new_info=department_update
    )
    

@departments_router.delete(
    "/{name}",
    response_model = schemas.Department,
    name="Delete deparment by name"
)
async def delete_deparment_by_name(
    name:str,
):
    """
    Delete deparment by name
    """
    return await deparment_web_crud.delete_enty_by_field(
        field="name",
        value_in=name
    )



    