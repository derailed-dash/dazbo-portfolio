import pytest
from fastapi.testclient import TestClient

def test_get_projects():
    from app.fast_api_app import app
    with TestClient(app) as client:
        response = client.get("/projects")
        assert response.status_code == 200

def test_get_blogs():
    from app.fast_api_app import app
    with TestClient(app) as client:
        response = client.get("/blogs")
        assert response.status_code == 200

def test_get_experience():
    from app.fast_api_app import app
    with TestClient(app) as client:
        response = client.get("/experience")
        assert response.status_code == 200
