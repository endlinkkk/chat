from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient

from application.api.main import create_application
from domain.entities.users import Credentials, User
from domain.values.users import Password, Phone, Username
from logic.init import init_container
from settings.config import AuthJWT
from tests.fixtures import init_dummy_container

import pytest
import jwt


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_application()
    app.dependency_overrides[init_container] = init_dummy_container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope="function")
def user() -> User:
    username = Username(value="user")
    phone = Phone(value="+79010000000")
    password = Password(value="alpine1212")
    crd = Credentials(phone=phone, password=password)
    user = User(username=username, credentials=crd, is_confirmed=True)

    return user


@pytest.fixture
def jwt_token(user: User):
    secret_key = AuthJWT.private_key_path.read_text()
    algorithm = AuthJWT.algorithm

    payload = {"sub": user.oid, "exp": datetime.now() + timedelta(hours=1)}

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token
