from datetime import date

from pydantic import BaseModel


# Shared properties
class AssignmentBase(BaseModel):
    name: str | None = None
    start_date: date | None = None
    final_date: date | None = None


# Properties to receive via API on creation
class AssignmentCreate(AssignmentBase):
    start_date: date
    final_date: date
    collaborator_id: int
    project_id: int


# Properties to receive via API on update
class AssignmentUpdate(AssignmentBase):
    pass


# Properties shared by models stored in DB
class AssignmentInDBBase(AssignmentBase):
    id: int | None = None
    collaborator_id: int | None = None
    project_id: int | None = None


# Properties to return via API
class Assignment(AssignmentInDBBase):
    pass