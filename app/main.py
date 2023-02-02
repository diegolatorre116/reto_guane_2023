import logging

from fastapi import FastAPI

from app.db.database import init_db
from app.api.api import api_router

log = logging.getLogger("uvicorn")

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(api_router, prefix="/api")

    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    # Integrating Tortoise-ORM
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")