from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from google.genai import types

from app.agent import PortfolioAgent
from app.fast_api_app import app


def test_chat_streaming_endpoint():
    # Mock the Gemini model response
    mock_response = MagicMock()
    mock_response.content = types.Content(role="model", parts=[types.Part.from_text(text="I am Dazbo's assistant.")])
    mock_response.partial = True

    async def mock_run_async(*args, **kwargs):
        yield mock_response

    # Mock the Firestore services to avoid needing a live DB during integration test
    with (
        patch("app.fast_api_app.ProjectService") as MockProjectService,
        patch("app.fast_api_app.BlogService") as MockBlogService,
        patch("app.fast_api_app.ExperienceService") as MockExperienceService,
        patch("app.tools.portfolio_search.ProjectService") as ToolMockProjectService,
        patch("app.tools.portfolio_search.BlogService") as ToolMockBlogService,
        patch("app.fast_api_app.get_client", new_callable=MagicMock) as MockGetClient,
        patch.object(PortfolioAgent, "run_async", side_effect=mock_run_async),
    ):
        # Setup mocks to return awaitable AsyncMocks
        MockProjectService.return_value.list = AsyncMock(return_value=[])
        MockBlogService.return_value.list = AsyncMock(return_value=[])
        MockExperienceService.return_value.list = AsyncMock(return_value=[])

        ToolMockProjectService.return_value.list = AsyncMock(return_value=[])
        ToolMockBlogService.return_value.list = AsyncMock(return_value=[])

        # Setup MockGetClient to return an AsyncMock for the db client
        mock_db_client = AsyncMock()
        MockGetClient.return_value = mock_db_client

        # Mock the client close method to be synchronous (as per recent change)
        mock_db_client.close.return_value = None

        # Use TestClient as a context manager to trigger lifespan events
        with TestClient(app) as client:
            response = client.post(
                "/api/chat/stream",
                json={"user_id": "test_user", "message": "Tell me about your projects"},
            )
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

            # Check that we received some SSE data
            count = 0
            has_data = False
            for line in response.iter_lines():
                if line:
                    count += 1
                    if line.startswith("data:"):
                        has_data = True
                if count > 10:  # Don't wait forever
                    break

            assert has_data, "Expected SSE data starting with 'data:'"
