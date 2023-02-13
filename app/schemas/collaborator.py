from enum import Enum

from pydantic import BaseModel


class Genders(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

# Shared properties
class CollaboratorBase(BaseModel):
    name: str | None = None
    last_name: str | None = None
    gender: Genders | None = None
    age: int | None = None
    is_active: bool | None = None
    job_id: int | None = None


# Properties to receive via API on creation
class CollaboratorCreate(CollaboratorBase):
    name: str
    last_name:str
    job_id: int


# Properties to receive via API on update
class CollaboratorUpdate(CollaboratorBase):
    pass


# Properties shared by models stored in DB
class CollaboratorInDBBase(CollaboratorBase):
    id: int | None = None


# Properties to return via API
class Collaborator(CollaboratorInDBBase):
    pass