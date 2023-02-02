from fastapi import APIRouter

from app.api.endpoints import (
    security,
    departments,
    users, 
    jobs
)

api_router = APIRouter()


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