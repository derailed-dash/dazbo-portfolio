"""
Description: Tool for searching the portfolio.
Why: Allows the agent to find projects, blogs, and videos based on user queries.
How: Fetches all items from Firestore and filters them in-memory (for now).
"""

import logging

from app.services.blog_service import BlogService
from app.services.firestore import get_client
from app.services.project_service import ProjectService
from app.services.video_service import VideoService

logger = logging.getLogger(__name__)


async def search_portfolio(query: str) -> str:
    """
    Searches for projects, blogs, and videos matching the query (title, description, tags).

    Args:
        query: The search term (e.g., "python", "react").

    Returns:
        A formatted string of matching items.
    """
    logger.debug(f"Searching portfolio for: {query}")
    db = get_client()
    project_service = ProjectService(db)
    blog_service = BlogService(db)
    video_service = VideoService(db)

    # Fetch all items (optimization: use firestore queries later)
    projects = await project_service.list()
    blogs = await blog_service.list()
    videos = await video_service.list()
    logger.debug(f"Fetched {len(projects)} projects, {len(blogs)} blogs and {len(videos)} videos")

    results = []
    query_lower = query.lower()

    for p in projects:
        # Check title
        if query_lower in p.title.lower():
            url = p.repo_url or p.demo_url or "No URL"
            results.append(
                f"[Project] ID: {p.id} | Title: {p.title} | Desc: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})"
            )
            continue
        # Check tags
        if any(query_lower in t.lower() for t in p.tags):
            url = p.repo_url or p.demo_url or "No URL"
            results.append(
                f"[Project] ID: {p.id} | Title: {p.title} | Desc: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})"
            )
            continue
        # Check description
        if p.description and query_lower in p.description.lower():
            url = p.repo_url or p.demo_url or "No URL"
            results.append(
                f"[Project] ID: {p.id} | Title: {p.title} | Desc: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})"
            )
            continue

    for b in blogs:
        # Check title
        if query_lower in b.title.lower():
            results.append(
                f"[Blog] ID: {b.id} | Title: {b.title} | Summary: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags or [])})"
            )
            continue
        # Check tags
        if b.tags and any(query_lower in t.lower() for t in b.tags):
            results.append(
                f"[Blog] ID: {b.id} | Title: {b.title} | Summary: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags)})"
            )
            continue
        # Check summary
        if b.summary and query_lower in b.summary.lower():
            results.append(
                f"[Blog] ID: {b.id} | Title: {b.title} | Summary: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags or [])})"
            )
            continue
        # Check AI summary
        if b.ai_summary and query_lower in b.ai_summary.lower():
            results.append(
                f"[Blog] ID: {b.id} | Title: {b.title} | AI Summary: {b.ai_summary[:150]}... (URL: {b.url}, Tags: {', '.join(b.tags or [])})"
            )
            continue

    for v in videos:
        if query_lower in v.title.lower() or (v.description and query_lower in v.description.lower()):
            results.append(
                f"[Video] ID: {v.id} | Title: {v.title} | Desc: {v.description} (URL: {v.video_url}, Date: {v.publish_date})"
            )

    total_count = len(projects) + len(blogs) + len(videos)
    if not results:
        return f"No projects, blogs or videos found matching '{query}'. (Database contains {total_count} items total)"

    header = f"Found {len(results)} matching items (Database contains {total_count} items total):"
    return header + "\n" + "\n".join(results)
