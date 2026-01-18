"""
Description: End-to-End Integration tests for Ingestion.
Why: Verifies the full flow from CLI to Firestore (mocked) for multiple sources.
How: Mocks Firestore and Connector responses, then runs the CLI app.
"""

from unittest.mock import AsyncMock, MagicMock, patch

from typer.testing import CliRunner

import app.tools.ingest as ingest_module

runner = CliRunner()


@patch("app.tools.ingest.GitHubConnector")
@patch("app.tools.ingest.MediumConnector")
@patch("app.tools.ingest.DevToConnector")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_e2e_ingestion_flow(mock_firestore, mock_devto, mock_medium, mock_github):
    # Setup Data Mocks
    mock_gh_repo = MagicMock()
    mock_gh_repo.get.side_effect = lambda k: {
        "name": "TestRepo",
        "description": "Desc",
        "html_url": "http://gh.com/repo",
        "topics": ["test"],
    }.get(k)
    # The connector returns Project objects, so we should mock the connector methods to return Project objects
    # Wait, the CLI calls connector.fetch_repositories which returns [Project]
    # So we don't need to mock internal dicts of the connector, just the return of fetch_repositories

    from app.models.blog import Blog
    from app.models.project import Project

    mock_gh_instance = mock_github.return_value
    mock_gh_instance.fetch_repositories = AsyncMock(
        return_value=[
            Project(
                title="GH Project",
                description="Desc",
                repo_url="http://gh.com/repo",
                tags=["test"],
                source_platform="github",
                is_manual=False,
            )
        ]
    )

    mock_med_instance = mock_medium.return_value
    mock_med_instance.fetch_posts = AsyncMock(
        return_value=[
            Blog(
                title="Med Post",
                summary="Sum",
                date="2026-01-01",
                platform="Medium",
                url="http://med.com/post",
                source_platform="medium_rss",
                is_manual=False,
            )
        ]
    )

    mock_dev_instance = mock_devto.return_value
    mock_dev_instance.fetch_posts = AsyncMock(
        return_value=[
            Blog(
                title="Dev Post",
                summary="Sum",
                date="2026-01-02",
                platform="Dev.to",
                url="http://dev.to/post",
                source_platform="devto_api",
                is_manual=False,
            )
        ]
    )

    # Setup Firestore Mocks
    mock_db = mock_firestore.return_value
    mock_col = mock_db.collection.return_value

    # Mock list (stream) to return empty first (no existing)
    # Since we iterate with 'async for', stream() must return an async iterable
    async def async_iter():
        for _ in []:
            yield _

    mock_col.stream.return_value = async_iter()

    # Mock add (create)
    # Mock add (create) - now using document().set()
    mock_doc_ref = MagicMock()
    mock_doc_ref.set = AsyncMock()
    mock_col.document.return_value = mock_doc_ref

    # Invoke CLI
    result = runner.invoke(ingest_module.app, ["--github-user", "user", "--medium-user", "user", "--devto-user", "user"])

    assert result.exit_code == 0

    # Verify Interactions
    assert mock_gh_instance.fetch_repositories.called
    assert mock_med_instance.fetch_posts.called
    assert mock_dev_instance.fetch_posts.called

    # Verify Firestore calls
    # We expect 3 create calls (1 project, 2 blogs), which now use document().set()
    # The service calls collection("projects").document(slug).set(...)
    assert mock_doc_ref.set.call_count >= 3
