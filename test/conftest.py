import os

import pytest

os.environ["FASTAPI_CONFIG"] = "testing"  # noqa


@pytest.fixture
def settings():
    from app.config import settings as _settings
    return _settings


@pytest.fixture
def app(settings):
    from app.main import create_app

    app = create_app()
    from app.db.database import init_db
    init_db(app)
    return app


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)