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
        collaborator. Check below sample response for a better
        understanding
        """
        assignments = await self.model.filter(
            start_date__lte=final_filter,
            final_date__gte=start_filter
        ).prefetch_related("collaborator__job", "project").all().order_by("project_id")
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

"""
[
  {
    "project_id": 1,
    "project_name": "Project rock",
    "jobs_implicated": [
      {
        "start_date": "2023-02-10",
        "end_date": "2023-02-25",
        "job_id": 1,
        "job_name": "Backend",
        "collaborators": [
          {
            "id": 1,
            "name": "Martin",
            "lastname": "quintero",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 1,
                "id": 1,
                "start_date": "2023-02-10",
                "final_date": "2023-02-20",
                "name": "tarea de backend"
              },
              {
                "project_id": 1,
                "collaborator_id": 1,
                "id": 9,
                "start_date": "2023-03-11",
                "final_date": "2023-03-17",
                "name": "Tarea de backend 2"
              }
            ]
          },
          {
            "id": 2,
            "name": "Diego",
            "lastname": "latorre",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 2,
                "id": 2,
                "start_date": "2023-02-10",
                "final_date": "2023-02-25",
                "name": "tarea de backend"
              }
            ]
          }
        ]
      },
      {
        "start_date": "2023-02-10",
        "end_date": "2023-02-25",
        "job_id": 3,
        "job_name": "Data Science",
        "collaborators": [
          {
            "id": 3,
            "name": "Paola",
            "lastname": "asd",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 3,
                "id": 3,
                "start_date": "2023-02-10",
                "final_date": "2023-02-20",
                "name": "tarea de data science"
              }
            ]
          },
          {
            "id": 4,
            "name": "Leonardo",
            "lastname": "asd",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 4,
                "id": 4,
                "start_date": "2023-02-10",
                "final_date": "2023-02-25",
                "name": "tarea de data science"
              }
            ]
          }
        ]
      },
      {
        "start_date": "2023-02-20",
        "end_date": "2023-02-27",
        "job_id": 2,
        "job_name": "Frontend",
        "collaborators": [
          {
            "id": 5,
            "name": "Cesar",
            "lastname": "pachon",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 5,
                "id": 5,
                "start_date": "2023-02-20",
                "final_date": "2023-02-25",
                "name": "tarea de frontend"
              },
              {
                "project_id": 1,
                "collaborator_id": 5,
                "id": 6,
                "start_date": "2023-02-20",
                "final_date": "2023-02-28",
                "name": "tarea de frontend 2"
              }
            ]
          },
          {
            "id": 6,
            "name": "Mario",
            "lastname": "pachon",
            "assignments": [
              {
                "project_id": 1,
                "collaborator_id": 6,
                "id": 7,
                "start_date": "2023-02-16",
                "final_date": "2023-02-27",
                "name": "tarea de frontend 3"
              },
              {
                "project_id": 1,
                "collaborator_id": 6,
                "id": 8,
                "start_date": "2023-02-20",
                "final_date": "2023-02-27",
                "name": "tarea de frontend 5"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    "project_id": 2,
    "project_name": "adidas",
    "jobs_implicated": [
      {
        "start_date": "2023-03-11",
        "end_date": "2023-03-17",
        "job_id": 1,
        "job_name": "Backend",
        "collaborators": [
          {
            "id": 1,
            "name": "Martin",
            "lastname": "quintero",
            "assignments": [
              {
                "project_id": 2,
                "collaborator_id": 1,
                "id": 9,
                "start_date": "2023-03-11",
                "final_date": "2023-03-17",
                "name": "Tarea de backend"
              }
            ]
          }, 
      {
        "start_date": "2023-02-20",
        "end_date": "2023-02-27",
        "job_id": 2,
        "job_name": "Frontend",
        "collaborators": [
          {
            "id": 5,
            "name": "Cesar",
            "lastname": "pachon",
            "assignments": [
              {
                "project_id": 2,
                "collaborator_id": 5,
                "id": 6,
                "start_date": "2023-02-11",
                "final_date": "2023-02-25",
                "name": "tarea de frontend 10"
              }
            ]
          },
          {
            "id": 6,
            "name": "Mario",
            "lastname": "pachon",
            "assignments": [
              {
                "project_id": 2,
                "collaborator_id": 6,
                "id": 8,
                "start_date": "2023-02-20",
                "final_date": "2023-02-27",
                "name": "tarea de frontend 21"
              }
            ]
          }
        ]
      }
    ]
  }
]

"""