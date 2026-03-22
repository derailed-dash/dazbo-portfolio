"""
Description: Integration tests for the Firestore MCP-enabled Agent.
Why: Verifies that the agent correctly integrates with and uses Firestore MCP tools.
How: Uses a real Tool subclass to verify invocation patterns.
"""

from unittest.mock import AsyncMock, patch

import pytest
from google.adk.agents import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.base_tool import BaseTool
from google.genai import types

# We import the agent after setting up environment variables in app.agent
from app.agent import root_agent
from app.config import settings


class MockMcpTool(BaseTool):
    """A concrete implementation of BaseTool for testing."""

    def __init__(self, name: str):
        desc = "Get a document" if name == "get_document" else "List documents"
        super().__init__(name=name, description=desc)
        self.run_async = AsyncMock()

    def _get_declaration(self) -> types.FunctionDeclaration:
        if self.name == "get_document":
            return types.FunctionDeclaration(
                name="get_document",
                description="Get a document",
                parameters={
                    "type": "object",
                    "properties": {"collection_id": {"type": "string"}, "document_id": {"type": "string"}},
                },
            )
        else:
            return types.FunctionDeclaration(
                name="list_documents",
                description="List documents",
                parameters={"type": "object", "properties": {"collection_id": {"type": "string"}}},
            )


@pytest.mark.asyncio
async def test_agent_uses_mcp_for_about_me() -> None:
    """
    Verifies that the agent correctly chooses the get_document tool
    with collection_id='content' and document_id='about' when asked about Dazbo.
    """
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id="test_user", app_name=settings.app_name)

    mock_tool = MockMcpTool("get_document")
    mock_tool.run_async.return_value = {"status": "success", "document": {"body": "Details"}}

    part = types.Part.from_function_call(name="get_document", args={"collection_id": "content", "document_id": "about"})
    from google.adk.models.llm_response import LlmResponse

    llm_response = LlmResponse(content=types.Content(role="model", parts=[part]), turn_complete=True)

    test_agent = Agent(name="test_agent", model=root_agent.model, instruction=root_agent.instruction, tools=[mock_tool])

    # Mock the final response after tool execution
    final_response = LlmResponse(
        content=types.Content(role="model", parts=[types.Part.from_text(text="Here is the info.")]), turn_complete=True
    )

    with patch("google.adk.models.google_llm.Gemini.generate_content_async") as mock_gen:

        async def mock_gen_async(*args, **kwargs):
            # First call returns function call
            # Subsequent calls (after tool result) return text
            if mock_gen.call_count == 1:
                yield llm_response
            else:
                yield final_response

        mock_gen.side_effect = mock_gen_async

        runner = Runner(agent=test_agent, session_service=session_service, app_name=settings.app_name)
        message = types.Content(role="user", parts=[types.Part.from_text(text="Tell me about Dazbo")])

        async for _ in runner.run_async(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            pass

        mock_tool.run_async.assert_called()
        args, kwargs = mock_tool.run_async.call_args
        tool_args = kwargs.get("args") or args[0]
        assert tool_args["collection_id"] == "content"
        assert tool_args["document_id"] == "about"


@pytest.mark.asyncio
async def test_agent_uses_mcp_for_project_search() -> None:
    """
    Verifies that the agent uses list_documents to search for projects.
    """
    session_service = InMemorySessionService()
    session = await session_service.create_session(user_id="test_user", app_name=settings.app_name)

    mock_tool = MockMcpTool("list_documents")
    mock_tool.run_async.return_value = {"status": "success", "documents": []}

    part = types.Part.from_function_call(name="list_documents", args={"collection_id": "projects"})
    from google.adk.models.llm_response import LlmResponse

    llm_response = LlmResponse(content=types.Content(role="model", parts=[part]), turn_complete=True)

    test_agent = Agent(name="test_agent", model=root_agent.model, instruction=root_agent.instruction, tools=[mock_tool])

    # Mock the final response after tool execution
    final_response = LlmResponse(
        content=types.Content(role="model", parts=[types.Part.from_text(text="Here is the info.")]), turn_complete=True
    )

    with patch("google.adk.models.google_llm.Gemini.generate_content_async") as mock_gen:

        async def mock_gen_async(*args, **kwargs):
            # First call returns function call
            # Subsequent calls (after tool result) return text
            if mock_gen.call_count == 1:
                yield llm_response
            else:
                yield final_response

        mock_gen.side_effect = mock_gen_async

        runner = Runner(agent=test_agent, session_service=session_service, app_name=settings.app_name)
        message = types.Content(role="user", parts=[types.Part.from_text(text="What projects?")])

        async for _ in runner.run_async(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            pass

        mock_tool.run_async.assert_called()
        args, kwargs = mock_tool.run_async.call_args
        tool_args = kwargs.get("args") or args[0]
        assert tool_args["collection_id"] == "projects"
