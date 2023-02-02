from enum import Enum

from pydantic import BaseModel, EmailStr


class Roles(str, Enum):
    C_LEVEL = "C-LEVEL"
    LEADER = "LEADER"


# Shared properties
class UserBase(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    role: Roles | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str
    role: Roles
    department_id: int


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int | None = None
    department_id: int | None = None


# Properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
