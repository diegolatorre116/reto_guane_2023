from fastapi import APIRouter

from app.api.endpoints import (
    first_records,
    security,
    departments,
    users, 
    jobs,
    collaborator,
    project,
    assignment,
    announcement, 
    calendar
)

api_router = APIRouter()

api_router.include_router(
    first_records.start_router,
    prefix="/generate_data",
    tags=["start"]
)

api_router.include_router(
    security.security_router,
    prefix="/login",
    tags=["security"]
)

api_router.include_router(
    departments.departments_router,
    prefix="/deparments",
    tags=["deparments"]
)

api_router.include_router(
    users.users_router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    jobs.jobs_router,
    prefix="/jobs",
    tags=["jobs"]
)

api_router.include_router(
    collaborator.collaborators_router,
    prefix="/collaborators",
    tags=["collaborators"]
)

api_router.include_router(
    project.projects_router,
    prefix="/projects",
    tags=["projects"]
)

api_router.include_router(
    assignment.assignments_router,
    prefix="/assignments",
    tags=["assignments"]
)

api_router.include_router(
    announcement.announcements_router,
    prefix="/announcements",
    tags=["announcements"]
)

api_router.include_router(
    calendar.calendar_router,
    prefix="/calendar",
    tags=["calendar"]
)