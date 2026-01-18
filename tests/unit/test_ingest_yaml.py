"""
Description: Unit tests for YAML ingestion in CLI.
Why: Verifies that the CLI tool correctly parses YAML files and creates/updates resources.
How: Mocks file reading and Firestore services.
"""

from unittest.mock import AsyncMock, patch, mock_open
import pytest
from typer.testing import CliRunner

runner = CliRunner()

YAML_CONTENT = """
projects:
  - title: Manual Project
    description: A manually added project
    repo_url: https://github.com/user/manual
    tags: [manual, test]
    metadata_only: true

blogs:
  - title: Manual Blog
    summary: A manually added blog
    date: "2026-01-01"
    platform: External
    url: https://external.com/blog
    metadata_only: true
"""

@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_yaml(mock_firestore, mock_blog_service, mock_project_service):
    # Setup mocks
    mock_proj_svc = mock_project_service.return_value
    mock_proj_svc.create = AsyncMock()
    mock_proj_svc.list = AsyncMock(return_value=[])
    mock_proj_svc.update = AsyncMock()

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.create = AsyncMock()
    mock_blog_svc.list = AsyncMock(return_value=[])
    mock_blog_svc.update = AsyncMock()
    
    # Import app inside to ensure mocks are applied if needed, though patch handles it
    try:
        from app.tools.ingest import app
    except ImportError:
        pytest.fail("Could not import ingest app")

    with patch("builtins.open", mock_open(read_data=YAML_CONTENT)):
        # We need to invoke the app with --yaml-file
        result = runner.invoke(app, ["--yaml-file", "manual_resources.yaml"])
        
    assert result.exit_code == 0
    
    # Verify Project creation
    assert mock_proj_svc.create.called
    call_args = mock_proj_svc.create.call_args[0][0]
    assert call_args.title == "Manual Project"
    assert call_args.is_manual is True
    assert call_args.metadata_only is True
    
    # Verify Blog creation
    assert mock_blog_svc.create.called
    call_args_blog = mock_blog_svc.create.call_args[0][0]
    assert call_args_blog.title == "Manual Blog"
    assert call_args_blog.platform == "External"
    assert call_args_blog.is_manual is True
