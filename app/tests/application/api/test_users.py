from httpx import Response
from fastapi import status
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_sign_up_success(app: FastAPI, client: TestClient, faker: Faker):
    url = app.url_path_for("sign_up_handler")
    input_data = {
        "username": "string",
        "phone": "string",
        "password1": "string",
        "password2": "string",
    }
    response: Response = client.post(url=url, json=input_data)
    assert response.is_success

