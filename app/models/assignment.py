from tortoise import fields

from app.models.base_class import Base


class Assignment(Base):
    name = fields.CharField(max_length=64)
    start_date = fields.DateField(null=False)
    final_date = fields.DateField(null=False)

    # ORM relationship between Assignment and Collaborator entity
    collaborator = fields.ForeignKeyField(
        "models.Collaborator",
        related_name="assignments",
        on_delete=fields.CASCADE
    )

    # ORM relationship between Assignment and Project entity
    project = fields.ForeignKeyField(
        "models.Project",
        related_name="assignments",
        on_delete=fields.CASCADE
    )

