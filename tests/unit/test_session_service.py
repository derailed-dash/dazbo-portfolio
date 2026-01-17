from unittest.mock import MagicMock

import pytest
from google.adk.sessions import BaseSessionService


@pytest.mark.asyncio
async def test_firestore_session_service_import():
    try:
        from app.services.session_service import FirestoreSessionService  # noqa: F401
    except ImportError:
        pytest.fail("Could not import FirestoreSessionService")


@pytest.mark.asyncio
async def test_firestore_session_service_implements_base():
    try:
        from app.services.session_service import FirestoreSessionService
    except ImportError:
        return

    assert issubclass(FirestoreSessionService, BaseSessionService)


@pytest.mark.asyncio
async def test_firestore_session_service_methods():
    try:
        from app.services.session_service import FirestoreSessionService
    except ImportError:
        return

    mock_db = MagicMock()
    service = FirestoreSessionService(db=mock_db)

    # Check for expected methods
    assert hasattr(service, "create_session")
    assert hasattr(service, "get_session")
