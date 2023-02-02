from typing import Any, Generic, TypeVar, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.models.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        """CRUD object with default methods to Create, Read, Update,
        Delete (CRUD).
        **Parameters**
        * `model`: A Tortoise ORM model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model


    async def get_all(self) -> list[ModelType]:
        db_objs = await self.model.all().values()
        return db_objs
    
    async def get_by_field(
        self,
        field: str, 
        value: Any
        ) -> Optional[ModelType]:
        """
        Get by any field in the database, such as "name", "username",
        "email" etc.
        Returns 'None' when :attr:'CRUDBase.model' does not have attribute
        'field'.
        """
        try:
            db_obj = await self.model.filter(**{field:value}).first().values()
        except Exception:
            return None
        
        return db_obj

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        await db_obj.save()
        return db_obj

    async def update_by_field(
        self,
        field: str,
        value: Any,
        obj_in: UpdateSchemaType | dict
        ) -> dict:
        """
        Update by any field in the database, such as "name", "username",
        "email" etc.
        Returns 'None' when :attr:'CRUDBase.model' does not have attribute
        'field'.
        """
        data_update = jsonable_encoder(obj_in, exclude_unset=True)      
        try:
            db_obj_update = await self.model.filter(**{field:value})\
            .update(**data_update)   
        except Exception:
            return None

        """Raise Exception when the "value" of field does not exist in the 
        database"""
        if not db_obj_update:
            raise Exception("The value of field doesn't exist in the database")
        else:
            return data_update

    async def remove_by_field(
        self,
        field: str,
        value: Any
        ) -> ModelType:
        """
        Delete by any field in the database, such as "name", "username",
        "email" etc.
        Returns 'None' when :attr:'CRUDBase.model' does not have attribute
        'field'.
        """
        try:
            obj = await self.model.filter(**{field:value}).first()
        except Exception:
            return None
        await obj.delete()
        return obj
        