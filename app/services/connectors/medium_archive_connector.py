"""
Description: Medium archive ingestion connector.
Why: Parses Medium export zip files to retrieve full blog history and content.
How: Uses zipfile, BeautifulSoup for HTML parsing, and markdownify for markdown conversion.
"""

import zipfile
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from app.models.blog import Blog
from app.services.content_enrichment_service import ContentEnrichmentService


class MediumArchiveConnector:
    def __init__(self, ai_service: ContentEnrichmentService | None = None):
        self.ai_service = ai_service or ContentEnrichmentService()

    async def fetch_posts(self, zip_path: str) -> list[Blog]:
        """
        Parses a Medium export zip file and returns a list of Blog models.
        """
        blogs = []
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                # Medium exports posts in the 'posts/' directory as HTML files
                post_files = [f for f in z.namelist() if f.startswith("posts/") and f.endswith(".html")]

                for post_file in post_files:
                    with z.open(post_file) as f:
                        html_content = f.read().decode("utf-8")
                        blog = await self._parse_html(html_content)
                        if blog:
                            blogs.append(blog)
        except Exception as e:
            print(f"Error reading Medium archive {zip_path}: {e}")

        return blogs

    async def _parse_html(self, html_content: str) -> Blog | None:
        """
        Parses a single Medium post HTML file.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Metadata extraction based on Medium's export format
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "Untitled"

        # Link / URL
        url_tag = soup.find("a", class_="u-url")
        url = url_tag["href"] if url_tag and url_tag.has_attr("href") else ""

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
        if tags_list:
            tags = [li.text for li in tags_list.find_all("li")]

        # Content - Medium wraps the main content in section.e-content
        content_section = soup.find("section", class_="e-content")
        if not content_section:
            return None

        # Paywall detection (Heuristic)
        is_private = "Member-only story" in content_section.get_text()

        # Convert content to Markdown
        # Markdownify rules: h1 -> #, h2 -> ##, h3 -> ###
        markdown_body = md(
            str(content_section),
            heading_style="ATX",
            bullets="-",
        )

        # Cleanup markdown headings if they are not ATX style (some older versions of markdownify)
        # Ensure #, ##, ### are used.

        # Frontmatter
        frontmatter = "---\n"
        frontmatter += f"title: {title}\n"
        if subtitle:
            frontmatter += f"subtitle: {subtitle}\n"
        if tags:
            frontmatter += f"tags: {', '.join(tags)}\n"
        frontmatter += "---\n\n"

        markdown_content = frontmatter + f"# {title}\n\n" + markdown_body

        # AI Summary
        ai_summary = None
        if self.ai_service:
            # Pass the text content for summarization
            ai_summary = await self.ai_service.generate_summary(content_section.get_text())

        return Blog(
            title=title,
            summary=subtitle or None,
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
