"""
Description: Unit tests for video ingestion synchronization (updates and deletions).
Why: Verifies that the CLI tool correctly identifies video replacements and stale entries.
How: Mocks VideoService and Typer confirmation prompts.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from typer.testing import CliRunner

from app.models.video import Video

runner = CliRunner()


@pytest.fixture
def mock_video_svc():
    with patch("app.tools.ingest.VideoService") as mock:
        svc = mock.return_value
        svc.list = AsyncMock()
        svc.update = AsyncMock()
        svc.delete = AsyncMock()
        svc.create = AsyncMock()
        yield svc


@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.firestore.AsyncClient")
@patch("typer.confirm")
def test_ingest_videos_replacement_detection(
    mock_confirm,
    mock_firestore,
    mock_project_service,
    mock_blog_service,
    mock_app_service,
    mock_video_svc,
):
    """
    Test that a video with a matching title but different URL is detected as a replacement.
    """
    # Setup existing video with same title but different URL
    existing_video = Video(
        id="youtube:old_id",
        title="Existing Video",
        description="Old description",
        video_url="https://www.youtube.com/watch?v=old_url",
        is_manual=True,
        source_platform="youtube",
    )
    mock_video_svc.list.return_value = [existing_video]
    # Also need empty lists for other collections during migration
    mock_app_service.return_value.list = AsyncMock(return_value=[])
    mock_blog_service.return_value.list = AsyncMock(return_value=[])
    mock_project_service.return_value.list = AsyncMock(return_value=[])

    mock_confirm.return_value = True

    from app.tools.ingest import app

    # Mock yaml.safe_load to return a video that shares a title but has a new URL
    yaml_data = {
        "videos": [
            {
                "title": "Existing Video",
                "description": "New description",
                "video_url": "https://www.youtube.com/watch?v=new_url",
            }
        ]
    }

    with patch("builtins.open", MagicMock()):
        with patch("app.tools.ingest.yaml.safe_load", return_value=yaml_data):
            result = runner.invoke(app, ["--yaml-file", "manual_videos.yaml"])

    assert result.exit_code == 0
    # Current implementation would NOT prompt because it only matches on URL
    # Failing test expects it to detect the title match and prompt for update
    assert mock_confirm.called
    assert mock_video_svc.update.called
    assert not mock_video_svc.create.called


@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.firestore.AsyncClient")
@patch("typer.confirm")
def test_ingest_videos_deletion_detection(
    mock_confirm,
    mock_firestore,
    mock_project_service,
    mock_blog_service,
    mock_app_service,
    mock_video_svc,
):
    """
    Test that a manual video entry in Firestore is prompted for deletion if missing from YAML.
    """
    # Existing video in Firestore (manual) but NOT in YAML
    existing_video = Video(
        id="youtube:missing_in_yaml",
        title="Stale Video",
        description="...",
        video_url="https://www.youtube.com/watch?v=stale",
        is_manual=True,
        source_platform="youtube",
    )
    mock_video_svc.list.return_value = [existing_video]
    mock_app_service.return_value.list = AsyncMock(return_value=[])
    mock_blog_service.return_value.list = AsyncMock(return_value=[])
    mock_project_service.return_value.list = AsyncMock(return_value=[])

    mock_confirm.return_value = True

    from app.tools.ingest import app

    # Empty YAML
    with patch("builtins.open", MagicMock()):
        with patch("app.tools.ingest.yaml.safe_load", return_value={"videos": []}):
            result = runner.invoke(app, ["--yaml-file", "manual_videos.yaml"])

    assert result.exit_code == 0
    # Failing test expects it to prompt for deletion
    assert mock_confirm.called
    assert mock_video_svc.delete.called


@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_videos_simulate_no_prompts(
    mock_firestore,
    mock_project_service,
    mock_blog_service,
    mock_app_service,
    mock_video_svc,
):
    """
    Test that --simulate mode does not trigger interactive prompts but logs intended actions.
    """
    existing_video = Video(
        id="youtube:old_id",
        title="Existing Video",
        description="Old description",
        video_url="https://www.youtube.com/watch?v=old_url",
        is_manual=True,
        source_platform="youtube",
    )
    mock_video_svc.list.return_value = [existing_video]
    mock_app_service.return_value.list = AsyncMock(return_value=[])
    mock_blog_service.return_value.list = AsyncMock(return_value=[])
    mock_project_service.return_value.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    yaml_data = {
        "videos": [
            {
                "title": "Existing Video",
                "description": "New description",
                "video_url": "https://www.youtube.com/watch?v=new_url",
            }
        ]
    }

    with patch("typer.confirm") as mock_confirm:
        with patch("builtins.open", MagicMock()):
            with patch("app.tools.ingest.yaml.safe_load", return_value=yaml_data):
                result = runner.invoke(
                    app, ["--yaml-file", "manual_videos.yaml", "--simulate"]
                )

    assert result.exit_code == 0
    assert not mock_confirm.called
    assert "Would update Video: Existing Video" in result.stdout
