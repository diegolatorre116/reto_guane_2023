import datetime

from tortoise.models import Model
from fastapi.encoders import jsonable_encoder

from app.models.announcement import Announcement
from app.schemas import AnnouncementCreate


class CRUDAnnouncement():
    def __init__(self, model: Model):
        """Object in charge of creating new announcements, get the
        announcements of the current day, and filter announcements by
        dates.
        **Parameters**
        * `model`: A Tortoise ORM model class
        """
        self.model = model
    
    async def create_announcement(self, obj_in: AnnouncementCreate):
        announcement_data = jsonable_encoder(obj_in)
        announcement_obj = self.model(**announcement_data)
        await announcement_obj.save()
        return announcement_obj

    async def today_announcement(self):
        today = datetime.datetime.now()
        return await self.model.filter(
            date__year=today.year,
            date__month=today.month,
            date__day=today.day
            ).all()

    async def announcements_between_dates(self, start_date, final_date):
        return await self.model.filter(
            date__range=(start_date, final_date)
            ).all()


announcement = CRUDAnnouncement(Announcement)