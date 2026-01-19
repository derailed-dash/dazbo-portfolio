"""
Description: Tool for getting detailed content information.
Why: Allows the agent to retrieve full details for a specific project or blog by ID.
How: Queries ProjectService and BlogService by ID.
"""

from google.cloud import firestore

from app.services.blog_service import BlogService
from app.services.project_service import ProjectService


async def get_content_details(item_id: str) -> str:
    """
    Retrieves full details for a specific project or blog by its ID.

    Args:
        item_id: The ID of the project or blog (e.g., "python-automation", "learning-python").

    Returns:
        A detailed string representation of the item, or a not found message.
    """
    db = firestore.AsyncClient()
    project_service = ProjectService(db)
    blog_service = BlogService(db)

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

    return f"Item with ID '{item_id}' not found in projects or blogs."
