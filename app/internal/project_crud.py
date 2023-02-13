from app.internal.CRUD.base_crud import CRUDBase
from app.schemas import ProjectCreate, ProjectUpdate
from app.models.project import Project


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_collaborators_by_project(self, project_id):
        """
        Get the collaborators of a project.
        :return: A list of collaborators of the project.
        """
        project = await self.model.get(id=project_id)
        collaborators = await project.collaborators.all()
        return collaborators

    async def get_asignments_by_project(self, project_id):
        """
        Get the collaborators of a project.
        :return: A list of assignments of the project.
        """
        project = await self.model.get(id=project_id)
        assignments = await project.assignments.all()
        return assignments


project = CRUDProject(Project)
