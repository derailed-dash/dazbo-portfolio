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


@pytest.mark.asyncio
async def test_fetch_posts_filtering_logic():
    # Mock JSON data: one normal post, one [Boost] post
    mock_json = [
        {
            "id": 1,
            "title": "Normal Post",
            "description": "Valid post",
            "published_at": "2026-01-01T10:00:00Z",
            "url": "https://dev.to/user/normal",
            "tag_list": [],
        },
        {
            "id": 2,
            "title": "[Boost] Quickie Post",
            "description": "Should be skipped",
            "published_at": "2026-01-02T10:00:00Z",
            "url": "https://dev.to/user/boost",
            "tag_list": [],
        },
    ]

    connector = DevToConnector()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json
        mock_get.return_value = mock_response

        blogs = await connector.fetch_posts("deraileddash")

        # Expect only the normal post
        assert len(blogs) == 1
        assert blogs[0].title == "Normal Post"


@pytest.mark.asyncio
async def test_fetch_posts_content_retrieval():
    # Mock List Response
    mock_list_json = [
        {
            "id": 1,
            "title": "Markdown Post",
            "description": "Post with markdown",
            "published_at": "2026-01-01T10:00:00Z",
            "url": "https://dev.to/user/md",
            "tag_list": [],
        }
    ]

    # Mock Detail Response
    mock_detail_json = {
        "id": 1,
        "title": "Markdown Post",
        "body_markdown": ("Word " * 210),
        # ... other fields
    }

    connector = DevToConnector()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        # Expect 2 calls: List and Detail

        # Setup side_effect for responses
        resp_list = MagicMock(spec=httpx.Response)
        resp_list.status_code = 200
        resp_list.json.return_value = mock_list_json

        resp_detail = MagicMock(spec=httpx.Response)
        resp_detail.status_code = 200
        resp_detail.json.return_value = mock_detail_json

        mock_get.side_effect = [resp_list, resp_detail]

        blogs = await connector.fetch_posts("deraileddash")

        assert len(blogs) == 1
        assert blogs[0].markdown_content == ("Word " * 210)

        # Verify calls
        assert mock_get.call_count == 2
