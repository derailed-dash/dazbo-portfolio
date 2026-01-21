"""
Description: Unit tests for GitHub Connector.
Why: Verifies that the GitHub connector correctly fetches repositories and maps them to Project models.
How: Mocks httpx.AsyncClient responses and asserts on the resulting Project objects.
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.connectors.github_connector import GitHubConnector


@pytest.mark.asyncio
async def test_fetch_repositories():
    # Mock data representing GitHub API response
    mock_repos = [
        {
            "id": 123,
            "name": "test-repo",
            "description": "A test repository",
            "html_url": "https://github.com/user/test-repo",
            "stargazers_count": 10,
            "language": "Python",
            "topics": ["python", "ai"],
            "private": False,
            "created_at": "2023-01-01T12:00:00Z",
        },
        {
            "id": 124,
            "name": "private-repo",
            "description": "A private repository",
            "html_url": "https://github.com/user/private-repo",
            "stargazers_count": 5,
            "language": "Go",
            "topics": ["go"],
            "private": True,
            "created_at": "2023-01-02T12:00:00Z",
        },
    ]

    connector = GitHubConnector()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_repos
        mock_get.return_value = mock_response

        projects = await connector.fetch_repositories("testuser")

        assert len(projects) == 1
        project = projects[0]
        assert project.title == "test-repo"
        assert project.description == "A test repository"
        assert project.repo_url == "https://github.com/user/test-repo"
        assert project.source_platform == "github"
        assert project.is_manual is False
        assert "python" in project.tags
        assert project.created_at == datetime(2023, 1, 1, 12, 0, 0, tzinfo=UTC)
