from tortoise.models import Model
from tortoise import fields

# Abstract model that will be the base of all the models
class Base(Model):
    'ORM base class'
    id = fields.IntField(pk = True)

    class Meta:
        abstract = True
