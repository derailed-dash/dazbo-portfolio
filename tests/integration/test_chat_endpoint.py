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
        mock_db_client = MagicMock()
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


def test_chat_streaming_endpoint_with_tool_call():
    # Mock the tool call event
    mock_tool_event = MagicMock()
    mock_tool_event.content = types.Content(
        role="model",
        parts=[types.Part(function_call=types.FunctionCall(name="search_portfolio", args={"query": "python"}))]
    )
    mock_tool_event.partial = False
    mock_tool_event.turn_complete = False

    # Mock the text response event
    mock_text_event = MagicMock()
    mock_text_event.content = types.Content(role="model", parts=[types.Part.from_text(text="I found some projects.")])
    mock_text_event.partial = True
    mock_text_event.turn_complete = False

    # Mock the final completion event
    mock_done_event = MagicMock()
    mock_done_event.partial = False
    mock_done_event.turn_complete = True

    async def mock_run_async(*args, **kwargs):
        yield mock_tool_event
        yield mock_text_event
        yield mock_done_event

    with (
        patch("app.fast_api_app.ProjectService") as _,
        patch("app.fast_api_app.BlogService") as _,
        patch("app.fast_api_app.ExperienceService") as _,
        patch("app.fast_api_app.get_client", new_callable=MagicMock) as MockGetClient,
        patch.object(PortfolioAgent, "run_async", side_effect=mock_run_async),
    ):
        mock_db_client = MagicMock()
        MockGetClient.return_value = mock_db_client
        mock_db_client.close.return_value = None

        with TestClient(app) as client:
            response = client.post(
                "/api/chat/stream",
                json={"user_id": "test_user", "message": "Search for python"},
            )
            assert response.status_code == 200

            lines = list(response.iter_lines())
            # We expect:
            # 1. Text chunk from mock_text_event
            # 2. [DONE] signal from mock_done_event (because turn_complete is True)

            has_text = any("I found some projects." in line for line in lines)
            has_done = any("data: [DONE]" in line for line in lines)

            assert has_text, "Should have received text content"
            assert has_done, "Should have received [DONE] signal"


def test_chat_streaming_endpoint_non_partial_multi_part():
    # Mock event with multiple text parts and partial=False
    mock_event = MagicMock()
    mock_event.content = types.Content(
        role="model",
        parts=[
            types.Part(text="Part1"),
            types.Part(text="Part2")
        ]
    )
    mock_event.partial = False
    mock_event.turn_complete = False

    # Mock final event
    mock_done_event = MagicMock()
    mock_done_event.partial = False
    mock_done_event.turn_complete = True

    async def mock_run_async(*args, **kwargs):
        yield mock_event
        yield mock_done_event

    with (
        patch("app.fast_api_app.ProjectService") as _,
        patch("app.fast_api_app.BlogService") as _,
        patch("app.fast_api_app.ExperienceService") as _,
        patch("app.fast_api_app.get_client", new_callable=MagicMock) as MockGetClient,
        patch.object(PortfolioAgent, "run_async", side_effect=mock_run_async),
    ):
        mock_db_client = MagicMock()
        MockGetClient.return_value = mock_db_client
        mock_db_client.close.return_value = None

        with TestClient(app) as client:
            response = client.post(
                "/api/chat/stream",
                json={"user_id": "test_user", "message": "Test"},
            )
            assert response.status_code == 200

            lines = list(response.iter_lines())
            # We assume app yields one event per "yield" call in generator if logical
            # But "Part1" and "Part2" are in ONE event.
            # So if code works, we get one data line: 'data: {"content": "Part1Part2"}'

            has_p1p2 = any("Part1Part2" in line for line in lines)
            assert has_p1p2, f"Expected content 'Part1Part2' in response lines: {lines}"
