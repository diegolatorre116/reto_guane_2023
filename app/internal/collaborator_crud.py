from typing import Any

from app.internal.CRUD.base_crud import CRUDBase
from app.schemas import CollaboratorCreate, CollaboratorUpdate
from app.models.collaborator import Collaborator


class CRUDCollaborator(CRUDBase[Collaborator, CollaboratorCreate, CollaboratorUpdate]):
    async def count_by_field(
        self,
        field:str,
        value:Any
        ) -> int:
        """
        Count the number of records in the Collaborator model based on a field and its value.
        :param field: The field to filter by.
        :param value: The value of the field to filter by.
        :return: The number of records that match the filter criteria.
        """
        total_objs = await self.model.filter(**{field:value}).all().count()
        return total_objs

    async def get_assignments_by_collaborator(self, collaborator_id):
        """
        Get the assignments of a collaborator.
        :return: A list of assignments of the collaborator.
        """
        collaborator = await self.model.get(id=collaborator_id)
        assignments = await collaborator.assignments.all()
        return assignments

    async def filter_availability(self, date, job_id):
        """
        Filter collaborators available for a specific day (that is,
        they do not have current assignments that day), based on their
        job_id.
        """
        collaborators_job = await self.model.filter(
            job_id=job_id
            ).prefetch_related("assignments").all()
        collaborators_avability = []
        for collaborator in collaborators_job:
            avalability = True
            for assignment in collaborator.assignments:
                if assignment.start_date <= date <= assignment.final_date:
                    avalability = False
                    break
            if avalability:
                collaborators_avability.append(collaborator)
        
        return collaborators_avability

                

collaborator = CRUDCollaborator(Collaborator)