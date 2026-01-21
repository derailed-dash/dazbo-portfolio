"""
Description: Dev.to ingestion connector.
Why: Fetches blog post metadata from Dev.to API to populate the portfolio.
How: Uses httpx to call Dev.to API and maps results to Blog model.
"""

import logging

import httpx

from app.models.blog import Blog

logger = logging.getLogger(__name__)


class DevToConnector:
    def __init__(self, base_url: str = "https://dev.to/api"):
        self.base_url = base_url

    async def fetch_posts(self, username: str, limit: int | None = None) -> list[Blog]:
        """
        Fetches blog posts for a given Dev.to username.
        """
        url = f"{self.base_url}/articles?username={username}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            articles_data = response.json()

            if limit:
                articles_data = articles_data[:limit]

            blogs = []
            for article in articles_data:
                title = article.get("title", "")
                if title.startswith("[Boost]"):
                    logger.info(f"Skipping (quickie): {title}")
                    continue

                # Fetch full article content to get markdown
                article_id = article.get("id")
                body_markdown = None
                if article_id:
                    try:
                        detail_url = f"{self.base_url}/articles/{article_id}"
                        detail_resp = await client.get(detail_url)
                        if detail_resp.status_code == 200:
                            body_markdown = detail_resp.json().get("body_markdown")
                    except Exception as e:
                        logger.warning(f"Failed to fetch content for article {article_id}: {e}")

                # Basic mapping
                # date is published_at, e.g. "2026-01-18T10:00:00Z"
                date_iso = article.get("published_at", "").split("T")[0]
                tags = article.get("tag_list", [])

                blog = Blog(
                    title=title,
                    summary=article.get("description") or "",
                    date=date_iso,
                    platform="Dev.to",
                    url=article.get("url"),
                    source_platform="devto_api",
                    is_manual=False,
                    markdown_content=body_markdown,
                    tags=tags,
                )
                blogs.append(blog)

        return blogs
