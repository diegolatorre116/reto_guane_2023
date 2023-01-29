from tortoise import fields

from app.models.base_class import Base


class Project(Base):
    name = fields.CharField(max_length=64)
    description = fields.TextField()
    customer = fields.CharField(max_length=64)
    start_date = fields.DateField(null=False)
    final_date = fields.DateField(null=False)