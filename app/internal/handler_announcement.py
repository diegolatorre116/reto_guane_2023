from abc import ABC, abstractmethod
from app.models.project import Project as ProjectModel
from app.models.collaborator import Collaborator as CollaboratorModel

class IInfoAnnouncement(ABC):
    """Interface for classes in charge of creating information for
    announcement.
    """    
    @abstractmethod
    async def create_name():
        pass

    @abstractmethod
    async def create_decription():
        pass


class InfoCollaboratorAnnouncement(IInfoAnnouncement):
    """
    Class responsible for creating the name and description for an
    announcement created when a collaborator is added or removed from
    a project.
    """    
    @staticmethod
    async def create_name():
        return "The collaborators of a project have been modified"

    @staticmethod
    async def create_description(
        user: dict,
        project_id: int,
        collaborator_id: int,
        action: str
        ):
        username = user["username"]
        project = await ProjectModel.filter(id=project_id).first()
        project_name = project.name

        collaborator = await CollaboratorModel.filter(
            id=collaborator_id
            ).first()
        collaborator_name = collaborator.name

        return f"The user:{username} has {action} collaborator:{collaborator_name}"\
            f" to the project:{project_name}"
        
        
    

        

