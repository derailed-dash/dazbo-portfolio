"""
Description: Unit tests for Hybrid Medium Ingestion (RSS + Archive).
Why: Verifies that metadata from RSS is prioritized over Archive, while content is kept.
How: Mocks connectors and services.
"""

from unittest.mock import AsyncMock, patch

import pytest

from app.models.blog import Blog
from app.tools.ingest import ingest_resources


@pytest.mark.asyncio
@patch("app.tools.ingest.zipfile.ZipFile")
@patch("app.tools.ingest.MediumConnector")
@patch("app.tools.ingest.MediumArchiveConnector")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.firestore.AsyncClient")
@patch("app.tools.ingest.ContentEnrichmentService")
async def test_medium_hybrid_logic(
    mock_enrichment_service,
    mock_firestore,
    mock_project_service,
    mock_blog_service,
    mock_archive_connector,
    mock_rss_connector,
    mock_zipfile,
):
    # Mock ZipFile to pass the file count check
    mock_zip = mock_zipfile.return_value.__enter__.return_value
    mock_zip.namelist.return_value = ["posts/test1.html", "posts/test2.html"]

    # Setup RSS blogs
    rss_blog = Blog(
        title="RSS Title",
        summary="RSS Summary",
        date="2026-01-20",
        platform="Medium",
        url="http://medium.com/test",
        source_platform="medium_rss",
        is_manual=False,
    )
    mock_rss_instance = mock_rss_connector.return_value
    mock_rss_instance.fetch_posts = AsyncMock(return_value=[rss_blog])

    # Setup Archive blogs (with same URL)
    archive_blog = Blog(
        title="Archive Title",
        summary="Archive Summary",
        date="2026-01-15",  # Older date
        platform="Medium",
        url="http://medium.com/test",
        source_platform="medium_archive",
        is_manual=False,
        markdown_content="# Markdown content",
        ai_summary="AI Summary",
        is_private=True,
    )

    # Another blog only in archive
    archive_only_blog = Blog(
        title="Archive Only",
        summary="Archive AI Summary",  # Connector should now set this
        date="2025-01-01",
        platform="Medium",
        url="http://medium.com/archive-only",
        source_platform="medium_archive",
        is_manual=False,
        markdown_content="# Archive Only content",
        ai_summary="Archive AI Summary",
    )

    # Define async generator for fetch_posts
    async def mock_fetch_posts(*args, **kwargs):
        yield "processed", archive_blog, "posts/test1.html"
        yield "processed", archive_only_blog, "posts/test2.html"

    mock_archive_instance = mock_archive_connector.return_value
    mock_archive_instance.fetch_posts = mock_fetch_posts

    mock_blog_svc_instance = mock_blog_service.return_value
    mock_blog_svc_instance.list = AsyncMock(return_value=[])
    mock_blog_svc_instance.create = AsyncMock()
    mock_blog_svc_instance.update = AsyncMock()

    # Run ingestion for Medium
    await ingest_resources(
        github_user=None,
        medium_user="testuser",
        medium_zip="test.zip",
        devto_user=None,
        yaml_file=None,
        about_file=None,
        project_id="test-project",
    )

    # Verify create calls
    # We expect 2 create calls
    assert mock_blog_svc_instance.create.call_count == 2

    # Get created blogs from call arguments
    created_blogs = [call.args[0] for call in mock_blog_svc_instance.create.call_args_list]

    # Check the merged blog (RSS + Archive)
    merged_blog = next(b for b in created_blogs if b.url == "http://medium.com/test")
    assert merged_blog.title == "RSS Title"  # RSS Priority
    assert merged_blog.date == "2026-01-20"  # RSS Priority
    assert merged_blog.markdown_content == "# Markdown content"  # Zip Enrichment
    assert merged_blog.ai_summary == "AI Summary"  # Zip Enrichment
    assert merged_blog.is_private is True  # Zip Enrichment (Heuristic)

    # Check the archive-only blog
    archive_only = next(b for b in created_blogs if b.url == "http://medium.com/archive-only")
    assert archive_only.title == "Archive Only"
    assert archive_only.summary == "Archive AI Summary"  # AI Summary
