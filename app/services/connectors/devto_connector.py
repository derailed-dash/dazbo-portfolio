"""
Description: Dev.to ingestion connector.
Why: Fetches blog post metadata from Dev.to API to populate the portfolio.
How: Uses httpx to call Dev.to API and maps results to Blog model.
"""

import httpx

from app.models.blog import Blog


class DevToConnector:
    def __init__(self, base_url: str = "https://dev.to/api"):
        self.base_url = base_url

    async def fetch_posts(self, username: str) -> list[Blog]:
        """
        Fetches blog posts for a given Dev.to username.
        """
        url = f"{self.base_url}/articles?username={username}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            articles_data = response.json()

        blogs = []
        for article in articles_data:
            # Basic mapping
            # date is published_at, e.g. "2026-01-18T10:00:00Z"
            date_iso = article.get("published_at", "").split("T")[0]

            blog = Blog(
                title=article.get("title"),
                summary=article.get("description") or "",
                date=date_iso,
                platform="Dev.to",
                url=article.get("url"),
                source_platform="devto_api",
                is_manual=False,
            )
            blogs.append(blog)

        return blogs
