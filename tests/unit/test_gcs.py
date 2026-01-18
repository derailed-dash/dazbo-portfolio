"""
Description: Unit tests for Google Cloud Storage utility.
Why: Verifies that the GCS helper class correctly interacts with the Google Cloud Storage library (mocked) and constructs public URLs.
How: Uses `unittest.mock` to mock `storage.Client` and assertions to verify bucket/blob interactions.
"""

from unittest.mock import MagicMock, patch

import pytest

# Will fail import until created
# from app.app_utils.gcs import GCSClient


@pytest.fixture
def mock_storage_client():
    with patch("google.cloud.storage.Client") as mock_client:
        yield mock_client


def test_upload_image(mock_storage_client):
    try:
        from app.app_utils.gcs import GCSClient
    except ImportError:
        pytest.fail("Could not import GCSClient")

    # Setup Mocks
    mock_bucket = MagicMock()
    mock_blob = MagicMock()

    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    # Configure public URL return
    mock_blob.public_url = "https://storage.googleapis.com/test-bucket/test.png"

    # Instantiate
    gcs = GCSClient(project_id="test-project", bucket_name="test-bucket")

    # Execute
    file_content = b"fake-image-content"
    url = gcs.upload_image(file_content, "test.png", "image/png")

    # Verify
    mock_storage_client.return_value.bucket.assert_called_with("test-bucket")
    mock_bucket.blob.assert_called_with("test.png")
    mock_blob.upload_from_string.assert_called_with(file_content, content_type="image/png")

    # Note: Depending on how we implement public URL construction (blob.public_url vs manual string format)
    # The spec says "bucket has correct public access policies", so manual string format is robust.
    # Standard public URL: https://storage.googleapis.com/<BUCKET_NAME>/<OBJECT_NAME>

    expected_url = "https://storage.googleapis.com/test-bucket/test.png"
    assert url == expected_url


def test_get_public_url():
    try:
        from app.app_utils.gcs import GCSClient
    except ImportError:
        pytest.fail("Could not import GCSClient")

    gcs = GCSClient(project_id="test-project", bucket_name="test-bucket")
    url = gcs.get_public_url("test.png")
    assert url == "https://storage.googleapis.com/test-bucket/test.png"
