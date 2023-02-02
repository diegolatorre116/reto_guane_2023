from typing import Optional, Any

from fastapi.encoders import jsonable_encoder

from app.internal.base_crud import CRUDBase
from app.schemas import UserCreate, UserUpdate
from app.models.user import User
from app.internal.base_crud import ModelType, CreateSchemaType, UpdateSchemaType
from app.core.security.pwd import password_hash
 

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """The create method is overridden to include password
        encryption.
        """
        obj_in_data = jsonable_encoder(obj_in)
        if 'password' in obj_in_data:
            obj_in_data['password'] = password_hash(obj_in_data['password'])
        db_obj = self.model(**obj_in_data)
        await db_obj.save()
        return db_obj

    async def update_by_field(
        self,
        field: str,
        value: Any,
        obj_in: UpdateSchemaType | dict
        ) -> dict:
        """The update_by_field method is overridden to include password
        encryption.
        Returns 'None' when :attr:'CRUDBase.model' does not have attribute
        'field'.
        """
        data_update = jsonable_encoder(obj_in, exclude_unset=True)
        if 'password' in data_update:
            data_update['password'] = password_hash(data_update['password'])
        try:
            db_obj_update = await self.model.filter(**{field:value})\
            .update(**data_update)   
        except Exception:
            return None
        
        """Raise Exception when the "value" of field does not exist in the 
        database"""
        if not db_obj_update:
            raise Exception
        else:
            return data_update
    
user = CRUDUser(User)

