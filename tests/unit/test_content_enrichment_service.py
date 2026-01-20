"""
Description: Unit tests for ContentEnrichmentService.
Why: Verifies that the AI service correctly interacts with the Gemini client.
How: Mocks the google-genai Client and asserts correct prompt generation and response handling.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.content_enrichment_service import ContentEnrichmentService


@pytest.mark.asyncio
async def test_enrich_content():
    # Mock the Client
    with patch("app.services.content_enrichment_service.Client") as MockClient:
        mock_client_instance = MockClient.return_value

        # Setup the mock for response.text
        mock_response = MagicMock()
        mock_response.text = '{"summary": "This is a test summary.", "tags": ["test"]}'

        # Setup the nested mock for await client.aio.models.generate_content(...)
        # client.aio.models.generate_content is an async method
        mock_client_instance.aio.models.generate_content = AsyncMock(return_value=mock_response)

        ai_service = ContentEnrichmentService()
        result = await ai_service.enrich_content("Some long blog post text.")

        assert result["summary"] == "This is a test summary."
        assert result["tags"] == ["test"]
        # Verify it was called with some content containing our text
        call_args = mock_client_instance.aio.models.generate_content.call_args
        assert "Some long blog post text." in call_args.kwargs["contents"]
