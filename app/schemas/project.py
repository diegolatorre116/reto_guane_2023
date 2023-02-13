from pydantic import BaseModel
from datetime import date

# Shared properties
class ProjectBase(BaseModel):
    name: str | None = None
    description: str | None = None
    customer: str | None = None
    start_date: date | None = None
    final_date: date | None = None


# Properties to receive via API on creation
class ProjectCreate(ProjectBase):
    name: str
    start_date: date
    final_date: date 


# Properties to receive via API on update
class ProjectUpdate(ProjectBase):
    pass


# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int | None = None


# Properties to return via API
class Project(ProjectInDBBase):
    pass

    