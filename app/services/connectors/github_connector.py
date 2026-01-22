"""
Description: GitHub ingestion connector.
Why: Fetches repository metadata from GitHub to populate the portfolio.
How: Uses httpx to call GitHub API and maps results to Project model.
"""

from datetime import datetime

import httpx

from app.models.project import Project


class GitHubConnector:
    def __init__(self, base_url: str = "https://api.github.com"):
        self.base_url = base_url

    async def fetch_repositories(self, username: str) -> list[Project]:
        """
        Fetches public repositories for a given GitHub username.
        """
        url = f"{self.base_url}/users/{username}/repos"
        params = {"type": "public"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            repos_data = response.json()

        projects = []
        for repo in repos_data:
            if repo.get("private") or repo.get("fork"):
                continue

            # Basic mapping
            project = Project(
                title=repo.get("name"),
                description=repo.get("description") or "",
                repo_url=repo.get("html_url"),
                tags=repo.get("topics") or [],
                source_platform="github",
                is_manual=False,
            )

            if created_at := repo.get("created_at"):
                project.created_at = datetime.fromisoformat(created_at)

            # Add language to tags if present
            if repo.get("language") and repo.get("language") not in project.tags:
                project.tags.append(repo.get("language").lower())

            projects.append(project)

        return projects
