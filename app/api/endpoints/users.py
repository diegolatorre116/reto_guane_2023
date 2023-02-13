from typing import Any

from fastapi import APIRouter, status, Depends

from app import internal, schemas
from app.core.auth.role_checker import allow_clevel

users_router = APIRouter()

user_web_crud = internal.WebCRUDWrapper(
    internal.user,
    enty_name="user"
    )


@users_router.get(
    "/",
    response_model= list[schemas.User],
    name="List all users"
)
async def get_users(current_user=Depends(allow_clevel)) -> Any:
    """
    Get a list all "user" entities. Allowed for "C-LEVEL".
    The return of the api has a following scheme:

    ```json
    [
    {
    "username": "guane",
    "email": "guane@example.com",
    "role": "C-LEVEL",
    "id": 1,
    "department_id": 1
    },
    {
    "username": "Daniel_10",
    "email": "daniel@example.com",
    "role": "LEADER",
    "id": 2,
    "department_id": 1
    }
    ...
    ]
    ``` 
    """
    return await user_web_crud.get_all_entries()


@users_router.get(
    "/{user_id}",
    response_model= schemas.User,
    name="User info by id"
)
async def get_user_id(user_id:int, current_user=Depends(allow_clevel)) -> Any:
    """
    Read one "user" entity based on its id. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "username": "guane",
    "email": "guane@example.com",
    "role": "C-LEVEL",
    "id": 1,
    "department_id": 1
    }
    ```
    """
    return await user_web_crud.get_enty_by_field("id", user_id)


@users_router.post(
    "/",
    response_model=schemas.User,
    name="Create new user",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: schemas.UserCreate, 
    current_user=Depends(allow_clevel)
    ) -> Any:
    """
    Create one "user" entity. There are two possible roles: "C-LEVEL" and
    "LEADER". The password will be stored encrypted in the database.
    The return of the api has a following scheme:
    ```json
    {
    "username": "Daniel_10",
    "email": "daniel@example.com",
    "role": "LEADER",
    "id": 2,
    "department_id": 1
    }
    ```
    """
    return await user_web_crud.post_enty(
        enty_info=user_in
    )


@users_router.patch(
    "/{user_id}",
    response_model = schemas.User,
    name="Update user by id"
)
async def update_user_id(
    user_id:int,
    user_update:schemas.UserUpdate,
    current_user=Depends(allow_clevel)
):
    """
    Update one "user" entity by id. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "username": "daniel_17",
    "email": null,
    "role": null,
    "id": null,
    "department_id": null
    }
    ```
    (In this example only the username was updated)
    """
    return await user_web_crud.update_enty_by_field(
        field="id",
        value_in=user_id,
        enty_new_info=user_update
    )
    

@users_router.delete(
    "/{user_id}",
    response_model = schemas.User,
    name="Delete user by id"
)
async def delete_user_by_username(
    user_id:str,
    current_user=Depends(allow_clevel)
):
    """
    Delete one "user" entity bases on its id. Allowed for "C-LEVEL".
    The return of the api has a following scheme:
    ```json
    {
    "username": "Daniel_10",
    "email": "daniel@example.com",
    "role": "LEADER",
    "id": 2,
    "department_id": 1
    }
    ```
    """
    return await user_web_crud.delete_enty_by_field(
        field="id",
        value_in=user_id
    )
