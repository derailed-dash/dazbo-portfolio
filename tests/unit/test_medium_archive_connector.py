"""
Description: Unit tests for MediumArchiveConnector.
Why: Verifies that Medium export zips are correctly parsed, converted to markdown, and summaries generated.
How: Mocks zipfile and ContentEnrichmentService to test the ingestion logic.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.connectors.medium_archive_connector import MediumArchiveConnector


@pytest.fixture
def mock_ai_service():
    service = MagicMock()
    service.enrich_content = AsyncMock(return_value={"summary": "Mocked summary", "tags": ["Python", "AI"]})
    return service


@pytest.mark.asyncio
async def test_parse_archive(mock_ai_service):
    # Mock zipfile
    with patch("zipfile.ZipFile") as MockZip:
        mock_zip_instance = MockZip.return_value.__enter__.return_value
        # Mock file list in zip
        mock_zip_instance.namelist.return_value = ["posts/2026-01-20_test-post.html"]

        # Mock HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Blog Title</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <article class="h-entry">
                <header>
                    <h1 class="p-name">Test Blog Title</h1>
                    <p class="p-summary">This is a subtitle</p>
                    <time class="dt-published" datetime="2026-01-20T12:00:00Z">Jan 20, 2026</time>
                </header>
                <section class="e-content">
                    <h1>Title in content</h1>
                    <h2>Heading 1</h2>
                    <h3>Subheading 1</h3>
                    <p>Some content with <a href="https://medium.com/p/123">Member-only story</a></p>
                </section>
                <footer>
                    <ul class="p-tags">
                        <li>Python</li>
                        <li>AI</li>
                    </ul>
                    <a class="u-url" href="https://medium.com/@user/test-post">Canonical URL</a>
                </footer>
            </article>
        </body>
        </html>
        """

        # Mock opening the file inside zip
        mock_zip_instance.open.return_value.__enter__.return_value.read.return_value = html_content.encode("utf-8")

        connector = MediumArchiveConnector(ai_service=mock_ai_service)
        blogs = []
        async for status, blog, _ in connector.fetch_posts("dummy_zip_path.zip"):
            if status == "processed" and blog:
                blogs.append(blog)

        assert len(blogs) == 1
        blog = blogs[0]

        assert blog.title == "Test Blog Title"
        assert blog.date == "2026-01-20"
        assert blog.platform == "Medium"
        assert blog.source_platform == "medium_archive"
        assert blog.is_private is True  # Detected from "Member-only story" text
        assert blog.ai_summary == "Mocked summary"
        assert "Python" in blog.tags
        assert "AI" in blog.tags

        # Check markdown conversion
        assert blog.markdown_content is not None
        assert "# Test Blog Title" in blog.markdown_content
        assert "## Heading 1" in blog.markdown_content
        assert "### Subheading 1" in blog.markdown_content
        # Title in content should also be H1 if it was h1 in HTML
        assert "# Title in content" in blog.markdown_content

        # Check frontmatter
        assert "subtitle: This is a subtitle" in blog.markdown_content
        assert "tags:" in blog.markdown_content
