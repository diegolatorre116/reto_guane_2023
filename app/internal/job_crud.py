from app.internal.base_crud import CRUDBase
from app.schemas import JobCreate, JobUpdate
from app.models.job import Job


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    pass

job = CRUDJob(Job)