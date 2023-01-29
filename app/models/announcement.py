from tortoise import fields

from app.models.base_class import Base


class Announcement(Base):
    name = fields.CharField(max_length=64)
    description = fields.TextField()
    date = fields.DatetimeField(auto_now=True)

    # ORM relationship between Announcement and User entity
    user_id = fields.ForeignKeyField(
        "models.User",
        related_name="announcements",
        on_delete=fields.CASCADE
    )



