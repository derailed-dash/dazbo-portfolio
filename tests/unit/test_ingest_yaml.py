"""
Description: Unit tests for YAML ingestion in CLI.
Why: Verifies that the CLI tool correctly parses YAML files and creates/updates resources.
How: Mocks file reading and Firestore services.
"""

from unittest.mock import AsyncMock, mock_open, patch

from typer.testing import CliRunner

runner = CliRunner()

YAML_CONTENT = """
projects:
  - id: explicit-proj-id
    title: Project With ID
    description: Proj
    repo_url: https://github.com/user/explicit

  - title: Project No ID
    description: Proj
    repo_url: https://github.com/user/fallback-repo
    metadata_only: true

  - title: Ambiguous Project
    description: Should be skipped
    metadata_only: true

blogs:
  - id: explicit-blog-id
    title: Blog With ID
    summary: Sum
    date: "2026-01-01"
    platform: External
    url: https://external.com/blog-url

  - title: Blog No ID
    summary: Sum
    date: "2026-01-01"
    platform: External
    url: https://external.com/fallback-blog
    metadata_only: true
"""


@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_yaml(mock_firestore, mock_blog_service, mock_project_service):
    # Setup mocks
    mock_proj_svc = mock_project_service.return_value
    mock_proj_svc.create = AsyncMock()

    # Mock existing projects with duplicates for Ambiguous Project
    from app.models.project import Project

    mock_proj_svc.list = AsyncMock(
        return_value=[
            Project(title="Ambiguous Project", description="Desc", id="dup-1"),
            Project(title="Ambiguous Project", description="Desc", id="dup-2"),
        ]
    )
    mock_proj_svc.update = AsyncMock()

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.create = AsyncMock()
    mock_blog_svc.list = AsyncMock(return_value=[])
    mock_blog_svc.update = AsyncMock()

    # Import app inside to ensure mocks are applied if needed, though patch handles it
    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_CONTENT)):
        # We need to invoke the app with --yaml-file
        result = runner.invoke(app, ["--yaml-file", "manual_resources.yaml"])

    assert result.exit_code == 0, f"CLI failed: {result.stdout}"

    # Verify we found projects
    assert "Found 3 manual projects" in result.stdout, f"Output: {result.stdout}"

    # Verify Project creation calls
    # Should have 2 calls
    assert mock_proj_svc.create.call_count == 2, (
        f"Expected 2 create calls, got {mock_proj_svc.create.call_count}. Output: {result.stdout}"
    )

    # 1. Explicit ID
    call_args_1 = mock_proj_svc.create.call_args_list[0]
    proj_1, kwargs_1 = call_args_1[0][0], call_args_1[1]
    assert proj_1.title == "Project With ID"
    assert kwargs_1["item_id"] == "explicit-proj-id"

    # 2. Fallback to Repo URL slug (fallback-repo -> fallback-repo)
    call_args_2 = mock_proj_svc.create.call_args_list[1]
    proj_2, kwargs_2 = call_args_2[0][0], call_args_2[1]
    assert proj_2.title == "Project No ID"
    assert kwargs_2["item_id"] == "manual:fallback-repo"

    # Verify Blog creation calls
    # Should have 2 calls
    assert mock_blog_svc.create.call_count == 2

    # 1. Explicit ID
    call_args_b1 = mock_blog_svc.create.call_args_list[0]
    blog_1, kwargs_b1 = call_args_b1[0][0], call_args_b1[1]
    assert blog_1.title == "Blog With ID"
    assert kwargs_b1["item_id"] == "explicit-blog-id"

    # 2. Fallback to URL slug (fallback-blog -> fallback-blog)
    call_args_b2 = mock_blog_svc.create.call_args_list[1]
    blog_2, kwargs_b2 = call_args_b2[0][0], call_args_b2[1]
    assert blog_2.title == "Blog No ID"
    assert kwargs_b2["item_id"] == "manual:fallback-blog"
