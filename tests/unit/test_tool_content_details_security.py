from unittest.mock import AsyncMock, patch

import pytest

from app.tools.content_details import get_content_details


@pytest.mark.asyncio
async def test_content_details_valid_id():
    """Test that a valid ID is processed correctly."""
    with patch("app.tools.content_details.ProjectService") as MockProjectService:
        # constant mock setup
        mock_service = AsyncMock()
        mock_service.get.return_value = None  # Valid ID but not found in project service for this test
        MockProjectService.return_value = mock_service

        with (
            patch("app.tools.content_details.BlogService") as MockBlogService,
            patch("app.tools.content_details.ContentService") as MockContentService,
            patch("app.tools.content_details.get_client"),
        ):
            MockBlogService.return_value.get = AsyncMock(return_value=None)
            MockContentService.return_value.get = AsyncMock(return_value=None)

            result = await get_content_details("valid-id_123")

            # Should have called the service (even if it returned None)
            mock_service.get.assert_called_once_with("valid-id_123")
            assert "not found" in result


@pytest.mark.asyncio
async def test_content_details_path_traversal():
    """Test that an ID with path traversal characters is rejected."""
    with patch("app.tools.content_details.ProjectService") as MockProjectService:
        mock_service = AsyncMock()
        MockProjectService.return_value = mock_service

        # We don't even need to mock other services if validation works early
        with patch("app.tools.content_details.get_client"):
            result = await get_content_details("invalid/path/traversal")

            # Should NOT call the service
            mock_service.get.assert_not_called()
            assert "Invalid item_id" in result


@pytest.mark.asyncio
async def test_content_details_malicious_chars():
    """Test that an ID with other malicious characters is rejected."""
    with patch("app.tools.content_details.ProjectService") as MockProjectService:
        mock_service = AsyncMock()
        MockProjectService.return_value = mock_service

        with patch("app.tools.content_details.get_client"):
            result = await get_content_details("../secrets")

            mock_service.get.assert_not_called()
            assert "Invalid item_id" in result
