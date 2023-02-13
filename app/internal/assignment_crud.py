from typing import TypeVar, Generic
from datetime import date

from fastapi.encoders import jsonable_encoder
from tortoise.models import Model
from tortoise.functions import Count

from app.internal.CRUD.base_crud import CRUDBase
from app.schemas import AssignmentCreate, AssignmentUpdate
from app.models.assignment import Assignment
from app.models.collaborator import Collaborator as CollaboratorModel
from app.models.assignment import Assignment

class CollaboratorNotInProject(Exception):
    pass

class CRUDAssignment(CRUDBase[Assignment, AssignmentCreate, AssignmentUpdate]):
    async def create(self, assignment_in: AssignmentCreate):
        """
        The create method is overridden to verify that the collaborator
        belongs to the project.
        In case of not belong, the exception will be raise:
        CollaboratorNotInProject
        """
        info_assignment = jsonable_encoder(assignment_in)
        collaborator_id = info_assignment["collaborator_id"]
        project_id = info_assignment["project_id"]
        
        collaborator = await CollaboratorModel.get(id=collaborator_id)
        if not await collaborator.projects.filter(id=project_id).exists():
            raise CollaboratorNotInProject(
                "The collaborator has not yet been assigned to the project"
            )

        assignment = self.model(**info_assignment)
        await assignment.save()
        return assignment
    

assignment = CRUDAssignment(Assignment)
