from datetime import date
from itertools import groupby

from tortoise.expressions import Q
from fastapi.encoders import jsonable_encoder

from app.models.assignment import Assignment


class AssignmentCalendar():
    def __init__(self, model: Assignment):
        self.model = model

    async def calendar(self, start_filter: date, final_filter:date):
        """
        Method to build the assignment calendar.
        **Parameters**
        * "start_filter": Start date to filter assignments
        * "final_filter": Final date to filter assignments
        :return: List of assignments that are valid during the date
        range between the start_date and final_date parameters.
        Assignments will be grouped by project, by job, and by
        collaborator.
        """
        assignments = await self.model.filter(
            start_date__lte=final_filter,
            final_date__gte=start_filter
        ).prefetch_related("collaborator__job", "project").all().order_by("project_id")
        calendar = []
        grouped_assignments = []
        for project, project_assignments in groupby(assignments, lambda x: x.project):
            project_group = {}
            project_group["project_id"] = project.id
            project_group["project_name"] = project.name
            project_group["jobs_implicated"] = []
            for job, job_assignments in groupby(project_assignments, lambda x: x.collaborator.job):
                info_job = {}
                copy_job_assignments = list(job_assignments)
                info_job["start_date"] = min([job.start_date for job in copy_job_assignments])
                info_job["end_date"] = max([job.final_date for job in copy_job_assignments])
                info_job["job_id"] = job.id
                info_job["job_name"] = job.name
                info_job["collaborators"] = []
                await job.fetch_related('collaborators')
                collaborators = job.collaborators
                for collaborator in collaborators:
                    await collaborator.fetch_related("assignments")
                    collaborator_info = {}
                    collaborator_info["id"] = collaborator.id
                    collaborator_info["name"] = collaborator.name
                    collaborator_info["lastname"] = collaborator.last_name
                    collaborator_info["assignments"] = [
                    assignment for assignment
                    in collaborator.assignments
                    if assignment.project_id == project.id
                    ]
                    info_job["collaborators"].append(collaborator_info)
                project_group["jobs_implicated"].append(info_job)
            grouped_assignments.append(project_group)
        return grouped_assignments


assignment_calendar = AssignmentCalendar(Assignment)

### Example method response: assignment calendar.calendar()