"""
Description: Unit tests for Ingestion Tool Refinement.
Why: Verifies platform-scoped IDs, metadata patching, and quickie filtering.
How: Uses pytest with mocks for services and connectors.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.blog import Blog
from app.models.project import Project

@pytest.mark.asyncio
@patch("app.tools.ingest.GitHubConnector")
@patch("app.tools.ingest.MediumConnector")
@patch("app.tools.ingest.DevToConnector")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
async def test_platform_scoped_ids(
    mock_firestore_client, mock_blog_service, mock_project_service, mock_devto, mock_medium, mock_github
):
    from app.tools.ingest import ingest_resources
    
    # Setup GitHub mock
    mock_gh_instance = mock_github.return_value
    mock_gh_instance.fetch_repositories = AsyncMock(return_value=[
        Project(title="My Project", description="Desc", repo_url="http://gh.com/p1", source_platform="github", tags=["test"])
    ])
    
    # Setup Blog mocks
    mock_med_instance = mock_medium.return_value
    mock_med_instance.fetch_posts = AsyncMock(return_value=[
        Blog(title="My Blog", summary="Sum", platform="Medium", url="http://med.com/b1", source_platform="medium_rss", date="2026-01-01")
    ])
    
    mock_dev_instance = mock_devto.return_value
    mock_dev_instance.fetch_posts = AsyncMock(return_value=[
        Blog(title="My Blog", summary="Sum", platform="Dev.to", url="http://dev.to/b1", source_platform="devto_api", date="2026-01-01", markdown_content="Long enough content " * 50)
    ])

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[])
    mock_blog_svc.create = AsyncMock()
    
    mock_proj_svc = mock_project_service.return_value
    mock_proj_svc.list = AsyncMock(return_value=[])
    mock_proj_svc.create = AsyncMock()

    await ingest_resources("user", "user", None, "user", None, None, "project")

    # Verify Project ID has prefix
    _, kwargs = mock_proj_svc.create.call_args
    assert kwargs["item_id"] == "github:my-project"

    # Verify Blog IDs have prefixes
    # Medium
    # We need to find the call for Medium
    medium_call = [c for c in mock_blog_svc.create.call_args_list if c[1]["item_id"].startswith("medium:")]
    assert len(medium_call) == 1
    assert medium_call[0][1]["item_id"] == "medium:my-blog"

    # Dev.to
    devto_call = [c for c in mock_blog_svc.create.call_args_list if c[1]["item_id"].startswith("devto:")]
    assert len(devto_call) == 1
    assert devto_call[0][1]["item_id"] == "devto:my-blog"

@pytest.mark.asyncio
@patch("app.tools.ingest.DevToConnector")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ContentEnrichmentService")
@patch("app.tools.ingest.firestore.AsyncClient")
async def test_metadata_patching(
    mock_firestore_client, mock_enrich_service, mock_blog_service, mock_devto
):
    from app.tools.ingest import ingest_resources
    
    # 1. Blog exists with ai_summary -> should skip enrichment
    existing_blog_with_summary = Blog(
        id="devto:exists", title="Existing", summary="Sum", platform="Dev.to", date="2026-01-01", url="http://dev.to/exists", ai_summary="Already here", source_platform="devto_api"
    )
    # 2. Blog exists without ai_summary -> should enrich
    existing_blog_no_summary = Blog(
        id="devto:patch", title="Patch Me", summary="Sum", platform="Dev.to", date="2026-01-01", url="http://dev.to/patch", source_platform="devto_api"
    )

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[existing_blog_with_summary, existing_blog_no_summary])
    mock_blog_svc.update = AsyncMock()
    mock_blog_svc.create = AsyncMock()
    mock_blog_svc.delete = AsyncMock()
    
    mock_dev_instance = mock_devto.return_value
    mock_dev_instance.fetch_posts = AsyncMock(return_value=[
        Blog(title="Existing", summary="Sum", platform="Dev.to", date="2026-01-01", url="http://dev.to/exists", source_platform="devto_api", markdown_content="Content " * 50),
        Blog(title="Patch Me", summary="Sum", platform="Dev.to", date="2026-01-01", url="http://dev.to/patch", source_platform="devto_api", markdown_content="Content " * 50)
    ])

    mock_enrich_instance = mock_enrich_service.return_value
    mock_enrich_instance.enrich_content = AsyncMock(return_value={"summary": "New Summary", "tags": ["test"]})

    await ingest_resources(None, None, None, "user", None, None, "project")

    # Verify enrichment called ONLY for "Patch Me"
    assert mock_enrich_instance.enrich_content.call_count == 1
    mock_enrich_instance.enrich_content.assert_called_once_with("Content " * 50)

    # Verify update called ONLY for "Patch Me"
    calls = mock_blog_svc.update.call_args_list
    assert len(calls) == 1
    
    # Check "Patch Me" update
    assert calls[0][0][0] == "devto:patch"
    assert calls[0][0][1]["ai_summary"] == "New Summary"

@pytest.mark.asyncio
@patch("app.services.connectors.devto_connector.httpx.AsyncClient")
async def test_devto_quickie_filtering(mock_httpx_client):
    from app.services.connectors.devto_connector import DevToConnector
    
    mock_client_instance = mock_httpx_client.return_value.__aenter__.return_value
    
    # Mock articles list
    mock_client_instance.get.side_effect = [
        # List response
        MagicMock(status_code=200, json=lambda: [
            {"id": 1, "title": "Full Article", "url": "http://dev.to/full", "published_at": "2026-01-01T10:00:00Z", "tag_list": ["test"]},
            {"id": 2, "title": "Quickie", "url": "http://dev.to/short", "published_at": "2026-01-01T10:00:00Z", "tag_list": ["test"]},
            {"id": 3, "title": "[Boost] something", "url": "http://dev.to/boost", "published_at": "2026-01-01T10:00:00Z", "tag_list": ["test"]}
        ]),
        # Detail 1: Full Article
        MagicMock(status_code=200, json=lambda: {"body_markdown": "Word " * 250}),
        # Detail 2: Quickie
        MagicMock(status_code=200, json=lambda: {"body_markdown": "Word " * 50}),
    ]

    connector = DevToConnector()
    blogs = await connector.fetch_posts("user")

    # Should only have "Full Article"
    # Boost is skipped by title, Quickie is skipped by word count
    assert len(blogs) == 1
    assert blogs[0].title == "Full Article"

