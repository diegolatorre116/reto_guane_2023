from datetime import date

from pydantic import BaseModel


# Shared properties
class AnnouncementBase(BaseModel):
    name: str | None = None
    description: str | None = None


# Properties to receive via API on creation
class AnnouncementCreate(AnnouncementBase):
    name: str
    user_id: int


# Properties shared by models stored in DB
class AnnouncementInDBBase(AnnouncementBase):
    id: int | None = None
    user_id: int | None = None


# Properties to return via API
class Announcement(AnnouncementInDBBase):
    pass