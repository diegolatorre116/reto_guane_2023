from app.internal.CRUD.base_crud import CRUDBase
from app.schemas import JobCreate, JobUpdate
from app.models.job import Job


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    """
    Get the collaborators of a job.
    :return: A list of collaborators of the project.
    """
    async def get_collaborators_by_job(self, job_id):
        job = await self.model.get(id=job_id)
        collaborators = await job.collaborators.all()
        return collaborators

job = CRUDJob(Job)