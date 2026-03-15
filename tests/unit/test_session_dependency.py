"""
Description: Unit tests for session service dependency injection.
Why: Verifies that the correct session service implementation is returned by the dependency provider.
How: Calls get_session_service with a mock request and checks the returned type.
"""

from unittest.mock import MagicMock

from google.adk.sessions import InMemorySessionService

from app.dependencies import get_session_service


def test_get_session_service_returns_in_memory():
    mock_request = MagicMock()
    mock_request.app.state.session_service = InMemorySessionService()

    service = get_session_service(mock_request)

    assert isinstance(service, InMemorySessionService)
