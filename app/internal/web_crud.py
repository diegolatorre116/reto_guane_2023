from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from app.internal.base_crud import CRUDBase
from app.models.base_class import Base


class WebCRUDWrapper:
    """Wrapper class to avoid duplicate code in API basic crud operations.
    """
    def __init__(
        self,
        crud: CRUDBase,
        *,
        enty_name: str
    ) -> None:
        self.crud = crud
        self.enty_name: str = enty_name.lower()
        self.enty_name_plural = self.enty_name + 's'

    async def get_all_entries(self) -> list[Base]:
        'Get all db entries of entity'
        all_enties = await self.crud.get_all()
        if len(all_enties) != 0:
            return all_enties
        else:
            raise HTTPException(
                400,
                detail=f'No {self.enty_name_plural} found'
            )

    async def get_enty_by_field(
        self, 
        field: str, 
        value_in: Any
        ) -> Base:
        enty_by_name = await self.crud.get_by_field(field, value_in)

        if not enty_by_name:
            raise HTTPException(
                400,
                detail=f'{self.enty_name.title()} with {field}:{value_in}' 
                    ' not found'
            )

        return enty_by_name

    async def post_enty(
        self,
        *,
        enty_info: BaseModel
    ) -> Base:
        try:
            created_enty = await self.crud.create(obj_in=enty_info)
        except Exception:
            raise HTTPException(
                500,
                detail=f'Error while creating {self.enty_name} in database' 
            )

        if not created_enty:
            raise HTTPException(
                400,
                detail=f'Create query of {self.enty_name} finished'  
                    ' but was not saves'
            )
        
        return created_enty

    async def update_enty_by_field(
        self,
        *,
        field: str,
        value_in: Any,
        enty_new_info: BaseModel
    ):
        try:
            updated_enty = await self.crud.update_by_field(
                field=field,
                value=value_in,
                obj_in=enty_new_info
            )
        except Exception:
            raise HTTPException(
                500,
                f'Error while updating {self.enty_name}:{value_in} in database.' 
                f' Probably the {self.enty_name} does not exist in database' 
            )
        
        if not updated_enty:
            raise HTTPException(
                400,
                f'{self.enty_name.title()} \'{value_in}\' was not updated.'
            )

        return updated_enty

    async def delete_enty_by_field(
        self,
        *,
        field: str,
        value_in: Any
    ):
        try:
            deleted_enty = await self.crud.remove_by_field(
                field=field,
                value=value_in
            )
        except Exception:
            raise HTTPException(
                500,
                f'Error while deleting {self.enty_name} with {field}: {value_in}' 
                f' from database. Probably the {self.enty_name} does' 
                ' not exist in database'
            )

        if not deleted_enty:
            raise HTTPException(
                400,
                f'{self.enty_name.title()} with {field}: {value_in} was not'
                ' deleted'
            )

        return deleted_enty