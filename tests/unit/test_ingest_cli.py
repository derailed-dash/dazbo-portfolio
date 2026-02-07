"""
Description: Unit tests for Ingest CLI.
Why: Verifies that the CLI tool correctly calls connectors and the Firestore service.
How: Mocks connector classes and Typer context.
"""

from unittest.mock import AsyncMock, patch

from typer.testing import CliRunner

runner = CliRunner()


@patch("app.tools.ingest.GitHubConnector")
@patch("app.tools.ingest.MediumConnector")
@patch("app.tools.ingest.DevToConnector")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_command(
    mock_firestore_client, mock_blog_service, mock_project_service, mock_devto, mock_medium, mock_github
):
    from app.models.blog import Blog
    from app.models.project import Project
    from app.tools.ingest import app

    # Setup mocks
    mock_gh_instance = mock_github.return_value
    mock_gh_instance.fetch_repositories = AsyncMock(
        return_value=[
            Project(
                title="Test Repo",
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
                title="Test Blog",
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
    mock_dev_instance.fetch_posts = AsyncMock(return_value=[])

    mock_proj_svc_instance = mock_project_service.return_value
    mock_proj_svc_instance.create = AsyncMock()
    mock_proj_svc_instance.list = AsyncMock(return_value=[])  # Mock existing items check if implemented

    mock_blog_svc_instance = mock_blog_service.return_value
    mock_blog_svc_instance.create = AsyncMock()
    mock_blog_svc_instance.list = AsyncMock(return_value=[])

    # Invoke CLI
    result = runner.invoke(app, ["--github-user", "testuser", "--medium-user", "testuser", "--devto-user", "testuser"])

    assert result.exit_code == 0
    mock_gh_instance.fetch_repositories.assert_called_once_with("testuser")
    mock_med_instance.fetch_posts.assert_called_once_with("testuser")
    mock_dev_instance.fetch_posts.assert_called_once_with("testuser", existing_urls=set())

    # Verify GitHub create called with slug
    # We expect create(project, item_id="github:test-repo")
    args, kwargs = mock_proj_svc_instance.create.call_args
    assert args[0].title == "Test Repo"
    assert kwargs.get("item_id") == "github:test-repo"

    # Verify Medium create called with slug
    # We expect create(blog, item_id="medium:test-blog")
    args, kwargs = mock_blog_svc_instance.create.call_args
    assert args[0].title == "Test Blog"
    assert kwargs["item_id"] == "medium:test-blog"
