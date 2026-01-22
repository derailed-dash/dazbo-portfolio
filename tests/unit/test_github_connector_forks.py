"""
Description: Unit tests for GitHub Connector fork filtering.
Why: Verifies that the GitHub connector skips repositories that are forks.
How: Mocks httpx.AsyncClient responses and asserts on the resulting Project objects.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.connectors.github_connector import GitHubConnector


@pytest.mark.asyncio
async def test_fetch_repositories_filters_forks():
    # Mock data representing GitHub API response with a fork
    mock_repos = [
        {
            "id": 123,
            "name": "original-repo",
            "description": "An original repository",
            "html_url": "https://github.com/user/original-repo",
            "private": False,
            "fork": False,
            "created_at": "2023-01-01T12:00:00Z",
        },
        {
            "id": 124,
            "name": "forked-repo",
            "description": "A forked repository",
            "html_url": "https://github.com/user/forked-repo",
            "private": False,
            "fork": True,
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

        # It should only return the original repo, not the fork
        assert len(projects) == 1
        assert projects[0].title == "original-repo"
