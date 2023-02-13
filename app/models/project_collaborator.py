from tortoise.models import Model
from tortoise import fields

# Intermediate table for the many-to-many relationship between
# collaborators and projects.
class ProjectCollaboratorModel(Model):
    project_id = fields.IntField()
    collaborator_id = fields.IntField()

    class Meta:
        table = 'project_collaborator'
        unique_together = (("project_id", "collaborator_id"),)
        
