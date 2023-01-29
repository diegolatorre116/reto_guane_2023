from enum import Enum

from tortoise import fields

from app.models.base_class import Base


class Roles(str, Enum):
    C_LEVEL = "C-LEVEL"
    LEADER = "LEADER"

class User(Base):
    username = fields.CharField(max_length=64, null=False)
    password = fields.CharField(max_length=128, null=False)
    email = fields.CharField(max_length=256)
    role = fields.CharEnumField(Roles)

    # ORM relationship between User and Department entity
    department_id = fields.ForeignKeyField(
        "models.Department",
        related_name="users",
        on_delete=fields.CASCADE
    )