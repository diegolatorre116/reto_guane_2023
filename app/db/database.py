import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# Necessary configuration for database migrations with aerich
TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": [
                "app.models.announcement",
                "app.models.assignment",
                "app.models.collaborator",
                "app.models.department",
                "app.models.job",
                "app.models.project",
                "app.models.user",
                "aerich.models"
                ],
            "default_connection": "default",
        },
    },
}

# Function to integrate Tortoise-ORM with FastAPI application
def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": [
            "app.models.announcement",
            "app.models.assignment",
            "app.models.collaborator",
            "app.models.department",
            "app.models.job",
            "app.models.project",
            "app.models.user"
            ]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
