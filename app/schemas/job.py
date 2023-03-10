from pydantic import BaseModel


# Shared properties
class JobBase(BaseModel):
    name: str | None = None
    description: str | None = None


# Properties to receive via API on creation
class JobCreate(JobBase):
    name: str
    department_id: int


# Properties to receive via API on update
class JobUpdate(JobBase):
    pass


# Properties shared by models stored in DB
class JobInDBBase(JobBase):
    id: int | None = None
    department_id: int | None = None


# Properties to return via API
class Job(JobInDBBase):
    pass