"""
Description: Tool for searching the portfolio.
Why: Allows the agent to find projects and blogs based on user queries.
How: Fetches all items from Firestore and filters them in-memory (for now).
"""

from google.cloud import firestore

from app.services.project_service import ProjectService
from app.services.blog_service import BlogService


async def search_portfolio(query: str) -> str:
    """
    Searches for projects and blogs matching the query (title, description, tags).
    
    Args:
        query: The search term (e.g., "python", "react").
        
    Returns:
        A formatted string of matching items.
    """
    db = firestore.AsyncClient()
    project_service = ProjectService(db)
    blog_service = BlogService(db)

    # Fetch all items (optimization: use firestore queries later)
    projects = await project_service.list()
    blogs = await blog_service.list()

    results = []
    query_lower = query.lower()

    for p in projects:
        # Check title
        if query_lower in p.title.lower():
            url = p.repo_url or p.demo_url or "No URL"
            results.append(f"[Project] {p.title}: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})")
            continue
        # Check tags
        if any(query_lower in t.lower() for t in p.tags):
            url = p.repo_url or p.demo_url or "No URL"
            results.append(f"[Project] {p.title}: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})")
            continue
        # Check description
        if p.description and query_lower in p.description.lower():
            url = p.repo_url or p.demo_url or "No URL"
            results.append(f"[Project] {p.title}: {p.description} (URL: {url}, Tags: {', '.join(p.tags)})")
            continue

    for b in blogs:
        # Check title
        if query_lower in b.title.lower():
            results.append(f"[Blog] {b.title}: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags or [])})")
            continue
        # Check tags
        if b.tags and any(query_lower in t.lower() for t in b.tags):
            results.append(f"[Blog] {b.title}: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags)})")
            continue
        # Check summary
        if b.summary and query_lower in b.summary.lower():
            results.append(f"[Blog] {b.title}: {b.summary} (URL: {b.url}, Tags: {', '.join(b.tags or [])})")
            continue

    if not results:
        return f"No projects or blogs found matching '{query}'."

    return "\n".join(results)
