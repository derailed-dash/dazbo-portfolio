"""
Description: Unit tests for "videos" YAML ingestion in CLI.
Why: Verifies that the CLI tool correctly parses the "videos" key in YAML and saves to Firestore.
How: Mocks file reading and VideoService.
"""

from unittest.mock import AsyncMock, mock_open, patch

from typer.testing import CliRunner

runner = CliRunner()

YAML_CONTENT_VIDEOS = """
videos:
  - title: "Cool YouTube Tutorial"
    description: "Learn how to build stuff."
    video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    thumbnail_url: "https://example.com/thumb.jpg"
    publish_date: "2024-01-01"
"""

@patch("app.tools.ingest.VideoService")
@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.ProjectService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_videos_yaml(mock_firestore, mock_project_service, mock_blog_service, mock_app_service, mock_video_service):
    mock_video_svc = mock_video_service.return_value
    mock_video_svc.create = AsyncMock()
    mock_video_svc.list = AsyncMock(return_value=[])
    mock_video_svc.update = AsyncMock()

    # Other services need to return empty lists for migration pass
    mock_app_service.return_value.list = AsyncMock(return_value=[])
    mock_blog_service.return_value.list = AsyncMock(return_value=[])
    mock_project_service.return_value.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_CONTENT_VIDEOS)):
        result = runner.invoke(app, ["--yaml-file", "manual_videos.yaml"])

    assert result.exit_code == 0
    assert "Found 1 manual videos" in result.stdout
    assert mock_video_svc.create.call_count == 1

    call_args = mock_video_svc.create.call_args
    video_obj = call_args[0][0]
    item_id = call_args[1]["item_id"]

    assert video_obj.title == "Cool YouTube Tutorial"
    assert video_obj.source_platform == "youtube"
    assert item_id == "youtube:dqw4w9wgxcq"
