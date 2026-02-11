"""
Description: Medium archive ingestion connector.
Why: Parses Medium export zip files to retrieve full blog history and content.
How: Uses zipfile, BeautifulSoup for HTML parsing, and markdownify for markdown conversion.
"""

import logging
import zipfile
from collections.abc import AsyncGenerator
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from app.models.blog import Blog
from app.services.content_enrichment_service import ContentEnrichmentService

logger = logging.getLogger(__name__)


class MediumArchiveConnector:
    def __init__(self, ai_service: ContentEnrichmentService):
        self.ai_service = ai_service

    async def fetch_posts(
        self, zip_path: str, existing_urls: set[str] | None = None, on_progress=None
    ) -> AsyncGenerator[tuple[str, Blog | None, str], None]:
        """
        Parses a Medium export zip file and yields processing status.
        Yields: (status, blog, filename)
        status: "processed", "skipped_draft", "skipped_not_blog", "skipped_existing", "error"
        """
        existing_urls = existing_urls or set()
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                # Medium exports posts in the 'posts/' directory as HTML files
                post_files = [f for f in z.namelist() if f.startswith("posts/") and f.endswith(".html")]
                total_files = len(post_files)

                for i, post_file in enumerate(post_files, 1):
                    # Check for draft in filename
                    if "draft_" in post_file.lower():
                        if on_progress:
                            on_progress(i, total_files, post_file, "Skipping draft")
                        yield "skipped_draft", None, post_file
                        continue

                    if on_progress:
                        on_progress(i, total_files, post_file, "Reading file")

                    try:
                        with z.open(post_file) as f:
                            html_content = f.read().decode("utf-8")
                            status, blog = await self._parse_html(
                                html_content, i, total_files, post_file, existing_urls, on_progress
                            )
                            yield status, blog, post_file

                    except Exception as e:
                        logger.error(f"Error processing file {post_file}: {e}")
                        yield "error", None, post_file
                        continue

        except Exception as e:
            logger.error(f"Error reading Medium archive {zip_path}: {e}")
            # Ensure we stop if the zip itself fails
            pass

    async def _parse_html(
        self, html_content: str, index: int, total: int, filename: str, existing_urls: set[str], on_progress=None
    ) -> tuple[str, Blog | None]:
        """
        Parses a single Medium post HTML file.
        Returns: (status, Blog)
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Skip comments and replies
        # 1. Medium often uses 'u-in-reply-to' class for replies
        if soup.find(class_="u-in-reply-to") or soup.find(class_="p-in-reply-to"):
            return "skipped_not_blog", None

        # 2. Content - Medium wraps the main content in section.e-content
        content_section = soup.find("section", class_="e-content")
        if not content_section:
            return "skipped_not_blog", None

        # 3. Heuristic: Real blogs in Medium export have subheadings (h3).
        # Comments and short replies typically do not.
        if not content_section.find("h3"):
            return "skipped_not_blog", None

        # Metadata extraction based on Medium's export format
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "Untitled"

        if on_progress:
            on_progress(index, total, filename, "Parsing content")

        # Link / URL
        url_tag = soup.find("a", class_="u-url")
        url = url_tag["href"] if url_tag and url_tag.has_attr("href") else ""

        if not url:
            # Fallback to canonical link often found in footer
            canonical_tag = soup.find("a", class_="p-canonical")
            if canonical_tag and canonical_tag.has_attr("href"):
                url = canonical_tag["href"]

        # Normalize URL: strip query parameters and trailing slashes
        if url:
            url = url.split("?")[0].rstrip("/")

        # Check if URL already exists
        if url and url in existing_urls:
            return "skipped_existing", None

        # Publication Date
        date_tag = soup.find("time", class_="dt-published")
        date_iso = ""
        if date_tag and date_tag.has_attr("datetime"):
            try:
                # Medium uses ISO format in datetime attribute
                dt = datetime.fromisoformat(date_tag["datetime"].replace("Z", "+00:00"))
                date_iso = dt.date().isoformat()
            except Exception:
                pass

        # Subtitle
        subtitle_tag = soup.find("p", class_="p-summary")
        subtitle = subtitle_tag.text if subtitle_tag else ""

        # Tags
        tags = []
        tags_list = soup.find("ul", class_="p-tags")
        if not tags_list:
            tags_list = soup.find("ul", class_="tags")  # Fallback class

        if tags_list:
            tags = [li.text for li in tags_list.find_all("li")]

        # Paywall detection (Heuristic)
        is_private = "Member-only story" in content_section.get_text()

        # Convert content to Markdown
        # Markdownify rules: h1 -> #, h2 -> ##, h3 -> ###
        markdown_body = md(
            str(content_section),
            heading_style="ATX",
            bullets="-",
        )

        # AI Enrichment (Summary and Tags)
        ai_summary = None
        if self.ai_service:
            if on_progress:
                on_progress(index, total, filename, "Processing content")

            enrichment_data = await self.ai_service.enrich_content(content_section.get_text())
            ai_summary = enrichment_data.get("summary")

            # Use AI tags if no tags found in HTML
            if not tags and enrichment_data.get("tags"):
                tags = enrichment_data.get("tags")

        # Fallback to AI summary if subtitle is missing
        final_summary = subtitle or ai_summary or None

        # Frontmatter
        frontmatter = "---\n"
        frontmatter += f"title: {title}\n"
        if date_iso:
            frontmatter += f"date: {date_iso}\n"
        if url:
            frontmatter += f"url: {url}\n"
        if final_summary:
            frontmatter += f"subtitle: {final_summary}\n"
        if tags:
            frontmatter += f"tags: {', '.join(tags)}\n"
        frontmatter += "---\n\n"

        markdown_content = frontmatter + f"# {title}\n\n" + markdown_body

        blog = Blog(
            title=title,
            summary=final_summary,
            date=date_iso,
            platform="Medium",
            url=url,
            source_platform="medium_archive",
            tags=tags,
            is_manual=False,
            is_private=is_private,
            markdown_content=markdown_content,
            ai_summary=ai_summary,
        )
        return "processed", blog
