from unittest.mock import AsyncMock, patch

import pytest

from app.models.blog import Blog
from app.models.project import Project

# We will implement this tool
from app.tools.content_details import get_content_details


@pytest.fixture
def mock_project():
    return Project(
        id="proj1",
        title="Python Automation",
        description="A generic python automation script",
        tags=["python", "automation"],
        repo_url="http://github.com/user/repo",
        demo_url="http://demo.com",
        image_url="http://img.com/1.png",
        featured=False,
    )


@pytest.fixture
def mock_blog():
    return Blog(
        id="blog1",
        title="Learning Python",
        summary="Intro to Python",
        url="http://medium.com/post1",
        date="2025-01-01",
        platform="Medium",
        tags=["python", "learning"],
    )


@pytest.mark.asyncio
async def test_get_content_details_found_in_projects(mock_project):
    with (
        patch("app.tools.content_details.ProjectService") as MockProjectService,
        patch("app.tools.content_details.BlogService") as MockBlogService,
        patch("app.tools.content_details.firestore.AsyncClient"),
    ):
        proj_service = AsyncMock()
        proj_service.get.return_value = mock_project
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        # Should not be called or return None if called (implementation detail, but let's say it's not reached if found)
        blog_service.get.return_value = None
        MockBlogService.return_value = blog_service

        result = await get_content_details("proj1")

        assert "Python Automation" in result
        assert "A generic python automation script" in result
        assert "http://github.com/user/repo" in result


@pytest.mark.asyncio
async def test_get_content_details_found_in_blogs(mock_blog):
    with (
        patch("app.tools.content_details.ProjectService") as MockProjectService,
        patch("app.tools.content_details.BlogService") as MockBlogService,
        patch("app.tools.content_details.firestore.AsyncClient"),
    ):
        proj_service = AsyncMock()
        proj_service.get.return_value = None
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.get.return_value = mock_blog
        MockBlogService.return_value = blog_service

        result = await get_content_details("blog1")

        assert "Learning Python" in result
        assert "Intro to Python" in result
        assert "http://medium.com/post1" in result


@pytest.mark.asyncio
async def test_get_content_details_not_found():
    with (
        patch("app.tools.content_details.ProjectService") as MockProjectService,
        patch("app.tools.content_details.BlogService") as MockBlogService,
        patch("app.tools.content_details.firestore.AsyncClient"),
    ):
        proj_service = AsyncMock()
        proj_service.get.return_value = None
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.get.return_value = None
        MockBlogService.return_value = blog_service

        result = await get_content_details("missing-id")

        assert "not found" in result.lower()
