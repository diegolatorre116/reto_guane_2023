from tortoise.models import Model

from app.models.project_collaborator import ProjectCollaboratorModel


class ProjectCollaborator():
    def __init__(self, model: Model):
        """Object in charge of add or remove collaborators to a
        project. Remember that the relationship between projects and 
        collaborators is many-to-many so the model of this class is
        the intermediate table: project_collaborator
        **Parameters**
        * `model`: A Tortoise ORM model class
        """
        self.model = model

    async def add_collaborator(
        self,
        project_id,
        collaborator_id
        ):
        db_obj = self.model(
            project_id=project_id,
            collaborator_id=collaborator_id
            )
        await db_obj.save()
        return db_obj

    async def remove_collaborator(
        self,
        project_id,
        collaborator_id
        ): 
        db_obj = await self.model.filter(
            project_id=project_id,
            collaborator_id=collaborator_id
        ).first()
        await db_obj.delete()
        return db_obj


project_collaborator_obj = ProjectCollaborator(ProjectCollaboratorModel)