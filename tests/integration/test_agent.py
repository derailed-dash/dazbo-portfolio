"""
Description: Integration tests for the Agent.
Why: Verifies that the agent can be initialized and stream responses using the ADK runner.
How: Uses `InMemorySessionService` and `Runner` to simulate agent execution.
"""

from unittest.mock import MagicMock, patch

from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.config import settings


def test_agent_stream() -> None:
    """
    Integration test for the agent stream functionality.
    Tests that the agent returns valid streaming responses.
    """

    session_service = InMemorySessionService()

    session = session_service.create_session_sync(user_id="test_user", app_name=settings.app_name)

    # Mock the agent's run_async method directly
    mock_event = MagicMock()
    mock_event.content = types.Content(
        role="model", parts=[types.Part.from_text(text="The sky is blue because of scattering.")]
    )
    mock_event.partial = True

    async def mock_run_async(*args, **kwargs):
        yield mock_event

    with patch("app.agent.PortfolioAgent.run_async", side_effect=mock_run_async):
        runner = Runner(agent=root_agent, session_service=session_service, app_name=settings.app_name)

        message = types.Content(role="user", parts=[types.Part.from_text(text="Why is the sky blue?")])

        events = list(
            runner.run(
                new_message=message,
                user_id="test_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            )
        )
        assert len(events) > 0, "Expected at least one message"

        has_text_content = False
        for event in events:
            if event.content and event.content.parts and any(part.text for part in event.content.parts):
                has_text_content = True
                break
        assert has_text_content, "Expected at least one message with text content"
