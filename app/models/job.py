from tortoise import fields

from app.models.base_class import Base


class Job(Base):
    name = fields.CharField(max_length=64, null=False)
    description = fields.TextField()

    # ORM relationship between Job and Department entity
    department = fields.ForeignKeyField(
        "models.Department",
        related_name="jobs",
        on_delete=fields.CASCADE
    )