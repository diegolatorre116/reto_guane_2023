from tortoise import fields

from app.models.base_class import Base


class Department(Base):
    name = fields.CharField(max_length=64, null=False)
    description = fields.TextField()