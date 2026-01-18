"""
Description: Unit tests for Dev.to Connector.
Why: Verifies that the Dev.to connector correctly fetches posts via API and maps them to Blog models.
How: Mocks httpx.AsyncClient responses with JSON and asserts on the resulting Blog objects.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.connectors.devto_connector import DevToConnector


@pytest.mark.asyncio
async def test_fetch_posts():
    # Mock JSON data from Dev.to API
    mock_json = [
        {
            "id": 12345,
            "title": "Test Dev.to Post",
            "description": "A description of the Dev.to post",
            "published_at": "2026-01-18T10:00:00Z",
            "url": "https://dev.to/user/test-devto-post",
            "tag_list": ["python", "webdev"],
        }
    ]

    connector = DevToConnector()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json
        mock_get.return_value = mock_response

        blogs = await connector.fetch_posts("deraileddash")

        assert len(blogs) == 1
        blog = blogs[0]
        assert blog.title == "Test Dev.to Post"
        assert blog.url == "https://dev.to/user/test-devto-post"
        assert blog.platform == "Dev.to"
        assert blog.source_platform == "devto_api"
        assert blog.is_manual is False
        assert blog.date.startswith("2026-01-18")
