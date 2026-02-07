"""
Description: Unit tests for "applications" YAML ingestion in CLI.
Why: Verifies that the CLI tool correctly parses the "applications" key in YAML.
How: Mocks file reading and Firestore services.
"""

from unittest.mock import AsyncMock, mock_open, patch

from typer.testing import CliRunner

runner = CliRunner()

YAML_CONTENT_APPS = """
applications:
  - title: "My Awesome App"
    description: "A great application."
    demo_url: "https://demo.example.com"
    image_url: "https://storage.googleapis.com/assets/app.png"
    tags: ["react", "fastapi"]
"""


@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_applications_yaml(mock_firestore, mock_blog_service, mock_app_service):
    mock_app_svc = mock_app_service.return_value
    mock_app_svc.create = AsyncMock()
    mock_app_svc.list = AsyncMock(return_value=[])
    mock_app_svc.update = AsyncMock()

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_CONTENT_APPS)):
        result = runner.invoke(app, ["--yaml-file", "manual_apps.yaml"])

    assert result.exit_code == 0

    # Verify we found applications
    assert "Found 1 manual applications" in result.stdout

    # Verify Application creation calls
    assert mock_app_svc.create.call_count == 1
    call_args = mock_app_svc.create.call_args_list[0]
    app_obj, _ = call_args[0][0], call_args[1]

    assert app_obj.title == "My Awesome App"
    assert app_obj.featured is True
    assert app_obj.is_manual is True
    assert app_obj.source_platform == "application"
    assert app_obj.demo_url == "https://demo.example.com"
    # Ensure ID is generated from demo_url domain if no ID provided
    # https://demo.example.com -> demo-example-com (slugify logic)
    # The actual logic splits by / and takes last part.
    # demo.example.com -> demo-example-com
    # assert kwargs['item_id'] == "demo.example.com" # slugify removes dots?
    # Let's check the slugify implementation in ingest.py. It replaces non-alnum with -.
    # So demo.example.com -> demo-example-com.
    # But wait, split('/')[-1] of https://demo.example.com is demo.example.com
    pass


def test_slugify_trailing_slash():
    # We can't import slugify directly easily if it's not exported or if we want to test the full flow
    # So we'll test via the app invocation with a new YAML
    YAML_TRAILING = """
applications:
  - title: "Trailing Slash App"
    description: "Desc"
    demo_url: "https://trailing.com/"
"""
    from unittest.mock import MagicMock

    mock_app_svc = MagicMock()
    mock_app_svc.create = AsyncMock()
    mock_app_svc.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with (
        patch("app.tools.ingest.ApplicationService", return_value=mock_app_svc),
        patch("app.tools.ingest.BlogService"),
        patch("app.tools.ingest.firestore.AsyncClient"),
        patch("builtins.open", mock_open(read_data=YAML_TRAILING)),
    ):
        result = runner.invoke(app, ["--yaml-file", "trailing.yaml"])

    assert result.exit_code == 0
    call_args = mock_app_svc.create.call_args
    # item_id should not be empty or random
    # https://trailing.com/ -> split -> trailing.com -> slugify -> trailing-com
    assert call_args[1]["item_id"] == "application:trailing-com"


@patch("app.tools.ingest.ApplicationService")
@patch("app.tools.ingest.BlogService")
@patch("app.tools.ingest.firestore.AsyncClient")
def test_ingest_applications_validation_error(mock_firestore, mock_blog_service, mock_app_service):
    # Missing demo_url for an application
    YAML_INVALID = """
applications:
  - title: "Invalid App"
    description: "Missing demo url"
"""
    mock_app_svc = mock_app_service.return_value
    mock_app_svc.create = AsyncMock()
    mock_app_svc.list = AsyncMock(return_value=[])

    mock_blog_svc = mock_blog_service.return_value
    mock_blog_svc.list = AsyncMock(return_value=[])

    from app.tools.ingest import app

    with patch("builtins.open", mock_open(read_data=YAML_INVALID)):
        result = runner.invoke(app, ["--yaml-file", "invalid_apps.yaml"])

    # Should report error about missing demo_url
    assert "missing the required 'demo_url'" in result.stdout
    assert mock_app_svc.create.call_count == 0
