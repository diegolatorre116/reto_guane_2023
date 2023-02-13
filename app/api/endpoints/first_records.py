from fastapi import APIRouter

from app.db.first_records import first_records

start_router = APIRouter()

@start_router.get(
    "/",
    name="Generate data"
)
async def generate_department_user():
    """
    Start here. This endpoint creates the first department and first
    user with role "C-LEVEL" to use the application. To see the
    information of these records, go to the file "readme.md" of the 
    repository.
    The return of the api should be:
    ```json
    "Done"
    ```
    """
    return await first_records()