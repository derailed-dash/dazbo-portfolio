"""
Description: Unit tests for Ingest CLI.
Why: Verifies that the CLI tool correctly calls connectors and the Firestore service.
How: Mocks connector classes and Typer context.
"""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from typer.testing import CliRunner
import app.tools.ingest

runner = CliRunner()

@patch("app.tools.ingest.GitHubConnector")
@patch("app.tools.ingest.MediumConnector")
@patch("app.tools.ingest.DevToConnector")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_command(
    mock_firestore_client,
    mock_blog_service,
    mock_project_service,
    mock_devto,
    mock_medium,
    mock_github
):
    try:
        from app.tools.ingest import app
    except ImportError:
        pytest.fail("Could not import ingest app")

    # Setup mocks
    mock_gh_instance = mock_github.return_value
    mock_gh_instance.fetch_repositories = AsyncMock(return_value=[])
    
    mock_med_instance = mock_medium.return_value
    mock_med_instance.fetch_posts = AsyncMock(return_value=[])
    
    mock_dev_instance = mock_devto.return_value
    mock_dev_instance.fetch_posts = AsyncMock(return_value=[])

    mock_proj_svc_instance = mock_project_service.return_value
    mock_proj_svc_instance.create = AsyncMock()
    mock_proj_svc_instance.list = AsyncMock(return_value=[]) # Mock existing items check if implemented
    
    mock_blog_svc_instance = mock_blog_service.return_value
    mock_blog_svc_instance.create = AsyncMock()
    mock_blog_svc_instance.list = AsyncMock(return_value=[])

    # Invoke CLI
    result = runner.invoke(app, ["--github-user", "testuser", "--medium-user", "testuser", "--devto-user", "testuser"])
    
    assert result.exit_code == 0
    mock_gh_instance.fetch_repositories.assert_called_once_with("testuser")
    mock_med_instance.fetch_posts.assert_called_once_with("testuser")
    mock_dev_instance.fetch_posts.assert_called_once_with("testuser")
