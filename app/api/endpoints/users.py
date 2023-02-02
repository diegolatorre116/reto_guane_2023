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
async def get_users() -> Any:
    """
    Get all users.
    """
    return await user_web_crud.get_all_entries()


@users_router.get(
    "/{username}",
    response_model= schemas.User,
    name="User info by username"
)
async def get_user_by_username(username:str) -> Any:
    """
    Get a specific user by username.
    """
    return await user_web_crud.get_enty_by_field("username", username)


@users_router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user_in: schemas.UserCreate) -> Any:
    """
    Create new user. There are two possible roles: "C-LEVEL" and
    "LEADER"
    """
    return await user_web_crud.post_enty(
        enty_info=user_in
    )


@users_router.patch(
    "/{username}",
    response_model = schemas.User,
    name="Update user by username"
)
async def update_user_by_username(
    username:str,
    user_update:schemas.UserUpdate
):
    """
    Update user by username
    """
    return await user_web_crud.update_enty_by_field(
        field="username",
        value_in=username,
        enty_new_info=user_update
    )
    

@users_router.delete(
    "/{username}",
    response_model = schemas.User,
    name="Delete user by username"
)
async def delete_user_by_username(
    username:str,
    current_user = Depends(allow_clevel)
):
    """
    Delete user by name
    """
    return await user_web_crud.delete_enty_by_field(
        field="username",
        value_in=username
    )
