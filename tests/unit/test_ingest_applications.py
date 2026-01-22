"""
Description: Unit tests for "applications" YAML ingestion in CLI.
Why: Verifies that the CLI tool correctly parses the "applications" key in YAML.
How: Mocks file reading and Firestore services.
"""

from unittest.mock import AsyncMock, mock_open, patch
from typer.testing import CliRunner
import pytest

runner = CliRunner()

YAML_CONTENT_APPS = """
applications:
  - title: "My Awesome App"
    description: "A great application."
    demo_url: "https://demo.example.com"
    image_url: "https://storage.googleapis.com/assets/app.png"
    tags: ["react", "fastapi"]
"""

@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_applications_yaml(mock_firestore, mock_blog_service, mock_project_service):
    mock_proj_svc = mock_project_service.return_value
    mock_proj_svc.create = AsyncMock()
    mock_proj_svc.list = AsyncMock(return_value=[])
    mock_proj_svc.update = AsyncMock()

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_CONTENT_APPS)):
        result = runner.invoke(app, ["--yaml-file", "manual_apps.yaml"])

    assert result.exit_code == 0
    
    # Verify we found applications (This might fail initially as the code only looks for 'projects' and 'blogs')
    assert "Found 1 manual applications" in result.stdout

    # Verify Project creation calls
    assert mock_proj_svc.create.call_count == 1
    call_args = mock_proj_svc.create.call_args_list[0]
    proj, kwargs = call_args[0][0], call_args[1]
    
    assert proj.title == "My Awesome App"
    assert proj.featured is True
    assert proj.is_manual is True
    assert proj.source_platform == "application"
    assert proj.demo_url == "https://demo.example.com"

@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_applications_validation_error(mock_firestore, mock_blog_service, mock_project_service):
    # Missing demo_url for an application
    YAML_INVALID = """
applications:
  - title: "Invalid App"
    description: "Missing demo url"
"""
    mock_proj_svc = mock_project_service.return_value
    mock_proj_svc.create = AsyncMock()
    mock_proj_svc.list = AsyncMock(return_value=[])

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_INVALID)):
        result = runner.invoke(app, ["--yaml-file", "invalid_apps.yaml"])

    # Should report error about missing demo_url
    assert "missing required demo_url" in result.stdout
    assert mock_proj_svc.create.call_count == 0
