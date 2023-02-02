from pydantic import BaseModel


# Shared properties
class DepartmentBase(BaseModel):
    name: str | None = None
    description: str | None = None


# Properties to receive via API on creation
class DepartmentCreate(DepartmentBase):
    name: str


# Properties to receive via API on update
class DepartmentUpdate(DepartmentBase):
    pass


# Properties shared by models stored in DB
class DepartmentInDBBase(DepartmentBase):
    id: int | None = None


# Properties to return via API
class Department(DepartmentInDBBase):
    pass