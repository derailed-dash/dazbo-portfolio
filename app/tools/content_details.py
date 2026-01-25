"""
Description: Tool for getting detailed content information.
Why: Allows the agent to retrieve full details for a specific project or blog by ID.
How: Queries ProjectService and BlogService by ID.
"""

import re

from app.services.blog_service import BlogService
from app.services.content_service import ContentService
from app.services.firestore import get_client
from app.services.project_service import ProjectService


async def get_content_details(item_id: str) -> str:
    """
    Retrieves full details for a specific project or blog by its ID.

    Args:
        item_id: The ID of the project or blog (e.g., "python-automation", "learning-python").

    Returns:
        A detailed string representation of the item, or a not found message.
    """
    # Security check: Validate item_id to prevent path traversal or injection
    if not re.match(r"^[a-zA-Z0-9_\-]+$", item_id):
        return f"Invalid item_id: '{item_id}'. IDs must contain only alphanumeric characters, underscores, and hyphens."

    db = get_client()
    project_service = ProjectService(db)
    blog_service = BlogService(db)
    content_service = ContentService(db)

    # Try finding in projects first
    project = await project_service.get(item_id)
    if project:
        details = [
            "Type: Project",
            f"Title: {project.title}",
            f"Description: {project.description}",
            f"Tags: {', '.join(project.tags)}",
        ]
        if project.repo_url:
            details.append(f"Repository URL: {project.repo_url}")
        if project.demo_url:
            details.append(f"Demo URL: {project.demo_url}")
        if project.image_url:
            details.append(f"Image URL: {project.image_url}")

        return "\n".join(details)

    # Try finding in blogs
    blog = await blog_service.get(item_id)
    if blog:
        details = [
            "Type: Blog",
            f"Title: {blog.title}",
            f"Summary: {blog.summary}",
            f"Platform: {blog.platform}",
            f"Date: {blog.date}",
            f"URL: {blog.url}",
            f"Tags: {', '.join(blog.tags)}",
        ]
        return "\n".join(details)

    # Try finding in general content (e.g. about page)
    content = await content_service.get(item_id)
    if content:
        details = [
            "Type: Page Content",
            f"Title: {content.title}",
            f"Last Updated: {content.last_updated}",
            "--- Content Body ---",
            content.body,
        ]
        return "\n".join(details)

    return f"Item with ID '{item_id}' not found in projects, blogs, or content pages."
