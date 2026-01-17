"""
Description: Integration tests for FastAPI application setup.
Why: Verifies that the application state is correctly initialized.
How: Uses `TestClient` to trigger lifespan events and checks `app.state`.
"""

from fastapi.testclient import TestClient


def test_app_state_firestore():
    from app.fast_api_app import app

    # Check if firestore_db is set in app.state
    # Note: State is usually initialized during lifespan
    # TestClient can trigger lifespan
    with TestClient(app) as client:
        assert hasattr(client.app.state, "firestore_db")
        assert hasattr(client.app.state, "project_service")
