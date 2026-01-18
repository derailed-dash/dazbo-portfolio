"""
Description: Unit tests for Medium Connector.
Why: Verifies that the Medium connector correctly fetches posts via RSS and maps them to Blog models.
How: Mocks httpx.AsyncClient responses with RSS XML and asserts on the resulting Blog objects.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.connectors.medium_connector import MediumConnector


@pytest.mark.asyncio
async def test_fetch_posts():
    # Mock RSS XML data
    mock_rss = """<?xml version="1.0" encoding="UTF-8"?>
    <rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">
      <channel>
        <title>Stories by Dazbo on Medium</title>
        <item>
          <title>Test Blog Post</title>
          <link>https://medium.com/@user/test-blog-post</link>
          <pubDate>Sun, 18 Jan 2026 10:00:00 GMT</pubDate>
          <content:encoded><![CDATA[<p>A summary of the post...</p>]]></content:encoded>
        </item>
      </channel>
    </rss>
    """

    connector = MediumConnector()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = mock_rss
        mock_get.return_value = mock_response

        blogs = await connector.fetch_posts("derailed.dash")

        assert len(blogs) == 1
        blog = blogs[0]
        assert blog.title == "Test Blog Post"
        assert blog.url == "https://medium.com/@user/test-blog-post"
        assert blog.platform == "Medium"
        assert blog.source_platform == "medium_rss"
        assert blog.is_manual is False
        assert blog.summary == "A summary of the post..."
        # Date should be ISO formatted
        assert blog.date.startswith("2026-01-18")
