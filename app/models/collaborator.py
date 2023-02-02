from enum import Enum

from tortoise import fields

from app.models.base_class import Base
from app.models.assignment import Assignment


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Collaborator(Base):
    name = fields.CharField(max_length=64, null=False)
    last_name = fields.CharField(max_length=64, null=False)
    gender = fields.CharEnumField(Gender)
    age = fields.IntField()
    is_active = fields.BooleanField(default=True)
    
    # ORM relationship between Collaborator and Job entity
    job = fields.ForeignKeyField(
        "models.Job",
        related_name="collaborators",
        on_delete=fields.RESTRICT
    )


