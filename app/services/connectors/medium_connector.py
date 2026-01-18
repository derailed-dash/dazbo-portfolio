"""
Description: Medium ingestion connector.
Why: Fetches blog post metadata from Medium RSS feed to populate the portfolio.
How: Uses httpx to fetch RSS and xml.etree.ElementTree to parse XML.
"""

import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import httpx

from app.models.blog import Blog


class MediumConnector:
    def __init__(self, feed_url_template: str = "https://medium.com/feed/@{username}"):
        self.feed_url_template = feed_url_template

    async def fetch_posts(self, username: str) -> list[Blog]:
        """
        Fetches blog posts from a given Medium username's RSS feed.
        """
        url = self.feed_url_template.format(username=username)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            rss_content = response.text

        root = ET.fromstring(rss_content)
        items = root.findall(".//item")

        blogs = []
        for item in items:
            title = item.find("title").text if item.find("title") is not None else "Untitled"
            link = item.find("link").text if item.find("link") is not None else ""
            pub_date_raw = item.find("pubDate").text if item.find("pubDate") is not None else ""

            # Convert RFC 2822 to ISO 8601
            try:
                date_dt = parsedate_to_datetime(pub_date_raw)
                date_iso = date_dt.date().isoformat()
            except Exception:
                date_iso = ""

            # Summary - extract from content:encoded
            content_encoded = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
            summary = ""
            if content_encoded is not None and content_encoded.text:
                # Simple HTML strip
                clean_text = re.sub(r"<[^>]+>", "", content_encoded.text)
                # Collapse whitespace
                clean_text = " ".join(clean_text.split())
                # Truncate to ~200 chars
                summary = clean_text[:200] + "..." if len(clean_text) > 200 else clean_text

            if not summary:
                summary = None

            blog = Blog(
                title=title,
                summary=summary,
                date=date_iso,
                platform="Medium",
                url=link,
                source_platform="medium_rss",
                is_manual=False,
            )
            blogs.append(blog)

        return blogs
