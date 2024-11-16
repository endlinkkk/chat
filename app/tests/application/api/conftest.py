from fastapi import FastAPI
from fastapi.testclient import TestClient

from application.api.main import create_application
from logic.init import init_container
from tests.fixtures import init_dummy_container

import pytest


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_application()
    app.dependency_overrides[init_container] = init_dummy_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
