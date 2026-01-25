"""
Description: Unit tests for Ingest CLI (About Page).
Why: Verifies that the CLI tool correctly handles the --about-file argument.
How: Mocks ContentService and Typer context.
"""

from unittest.mock import AsyncMock, patch, mock_open
from typer.testing import CliRunner

runner = CliRunner()

@patch("app.tools.ingest.ContentService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_about_file(mock_firestore_client, mock_content_service):
    from app.tools.ingest import app

    # Setup mocks
    mock_content_svc_instance = mock_content_service.return_value
    mock_content_svc_instance.create = AsyncMock()

    markdown_content = "# About Me\nThis is my bio."

    # Invoke CLI with --about-file
    with patch("builtins.open", mock_open(read_data=markdown_content)):
        result = runner.invoke(app, ["--about-file", "about.md"])

    print(result.stdout) # DEBUG
    assert result.exit_code == 0

    
    # Verify ContentService.create was called
    args, kwargs = mock_content_svc_instance.create.call_args
    content_obj = args[0]
    
    assert content_obj.title == "About"
    assert content_obj.body == markdown_content
    # Expect item_id="about"
    assert kwargs.get("item_id") == "about"

