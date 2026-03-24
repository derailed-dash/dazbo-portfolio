"""
Description: Unit tests for the search_portfolio tool.
Why: Verifies that the search tool correctly filters projects, blogs, and videos based on query strings.
How: Uses unittest.mock to simulate ProjectService, BlogService, and VideoService responses.
"""

from unittest.mock import AsyncMock, patch

import pytest

from app.models.blog import Blog
from app.models.project import Project
from app.models.video import Video
from app.tools.portfolio_search import search_portfolio


@pytest.fixture
def mock_projects():
    return [
        Project(
            id="proj1",
            title="Python Automation",
            description="A generic python automation script",
            tags=["python", "automation"],
            repo_url="http://github.com/user/repo",
            demo_url=None,
            image_url=None,
            featured=False,
        ),
        Project(
            id="proj2",
            title="React Dashboard",
            description="A dashboard built with React",
            tags=["react", "typescript"],
            repo_url="http://github.com/user/dashboard",
            demo_url=None,
            image_url=None,
            featured=True,
        ),
    ]


@pytest.fixture
def mock_blogs():
    return [
        Blog(
            id="blog1",
            title="Learning Python",
            summary="Intro to Python",
            url="http://medium.com/post1",
            date="2025-01-01",
            platform="Medium",
            tags=["python", "learning"],
        ),
        Blog(
            id="blog2",
            title="Advanced TypeScript",
            summary="Deep dive into TS",
            url="http://dev.to/post2",
            date="2025-01-02",
            platform="Dev.to",
            tags=["typescript", "web"],
        ),
    ]


@pytest.fixture
def mock_videos():
    return [
        Video(
            id="youtube:123",
            title="Introduction to ADK",
            description="A video overview of the Agent Development Kit.",
            video_url="https://youtube.com/watch?v=123",
            publish_date="2024-03-24",
            is_manual=True,
            source_platform="youtube",
        )
    ]


@pytest.mark.asyncio
async def test_search_portfolio_by_tag(mock_projects, mock_blogs, mock_videos):
    with (
        patch("app.tools.portfolio_search.ProjectService") as MockProjectService,
        patch("app.tools.portfolio_search.BlogService") as MockBlogService,
        patch("app.tools.portfolio_search.VideoService") as MockVideoService,
        patch("app.tools.portfolio_search.get_client"),
    ):
        # Setup mocks
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        video_service = AsyncMock()
        video_service.list.return_value = mock_videos
        MockVideoService.return_value = video_service

        # Test searching for "python"
        result = await search_portfolio("python")

        assert "Python Automation" in result
        assert "Learning Python" in result
        assert "React Dashboard" not in result


@pytest.mark.asyncio
async def test_search_portfolio_by_text(mock_projects, mock_blogs, mock_videos):
    with (
        patch("app.tools.portfolio_search.ProjectService") as MockProjectService,
        patch("app.tools.portfolio_search.BlogService") as MockBlogService,
        patch("app.tools.portfolio_search.VideoService") as MockVideoService,
        patch("app.tools.portfolio_search.get_client"),
    ):
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        video_service = AsyncMock()
        video_service.list.return_value = mock_videos
        MockVideoService.return_value = video_service

        # Test searching for "dashboard" (in title of project)
        result = await search_portfolio("Dashboard")

        assert "React Dashboard" in result
        assert "Python Automation" not in result


@pytest.mark.asyncio
async def test_search_portfolio_video_match(mock_projects, mock_blogs, mock_videos):
    with (
        patch("app.tools.portfolio_search.ProjectService") as MockProjectService,
        patch("app.tools.portfolio_search.BlogService") as MockBlogService,
        patch("app.tools.portfolio_search.VideoService") as MockVideoService,
        patch("app.tools.portfolio_search.get_client"),
    ):
        proj_service = AsyncMock()
        proj_service.list.return_value = []
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.list.return_value = []
        MockBlogService.return_value = blog_service

        video_service = AsyncMock()
        video_service.list.return_value = mock_videos
        MockVideoService.return_value = video_service

        # Test searching for "ADK" (in video title)
        result = await search_portfolio("ADK")

        assert "Introduction to ADK" in result
        assert "[Video]" in result


@pytest.mark.asyncio
async def test_search_portfolio_no_results(mock_projects, mock_blogs, mock_videos):
    with (
        patch("app.tools.portfolio_search.ProjectService") as MockProjectService,
        patch("app.tools.portfolio_search.BlogService") as MockBlogService,
        patch("app.tools.portfolio_search.VideoService") as MockVideoService,
        patch("app.tools.portfolio_search.get_client"),
    ):
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        video_service = AsyncMock()
        video_service.list.return_value = mock_videos
        MockVideoService.return_value = video_service

        result = await search_portfolio("java")

        assert "No projects, blogs or videos found" in result


@pytest.mark.asyncio
async def test_search_priority_and_deduplication(mock_projects):
    # Create blogs with matches in specific fields
    blogs = [
        Blog(title="Title Match", summary="no", url="u1", date="2025", platform="p", tags=["no"], ai_summary="no"),
        Blog(title="No", summary="no", url="u2", date="2025", platform="p", tags=["Tag Match"], ai_summary="no"),
        Blog(title="No", summary="Summary Match", url="u3", date="2025", platform="p", tags=["no"], ai_summary="no"),
        Blog(title="No", summary="no", url="u4", date="2025", platform="p", tags=["no"], ai_summary="AI Summary Match"),
        # Duplicate match candidates (should appear once)
        Blog(
            title="Double Match",
            summary="Double Match",
            url="u5",
            date="2025",
            platform="p",
            tags=["Double Match"],
            ai_summary="Double Match",
        ),
    ]

    with (
        patch("app.tools.portfolio_search.ProjectService") as MockProjectService,
        patch("app.tools.portfolio_search.BlogService") as MockBlogService,
        patch("app.tools.portfolio_search.VideoService") as MockVideoService,
        patch("app.tools.portfolio_search.get_client"),
    ):
        proj_service = AsyncMock()
        proj_service.list.return_value = []
        MockProjectService.return_value = proj_service

        blog_service = AsyncMock()
        blog_service.list.return_value = blogs
        MockBlogService.return_value = blog_service

        video_service = AsyncMock()
        video_service.list.return_value = []
        MockVideoService.return_value = video_service

        result = await search_portfolio("Match")

        # Verify all unique blogs are found
        assert "Title Match" in result
        assert "Tag Match" in result
        assert "Summary Match" in result
        assert "AI Summary Match" in result

        # Verify deduplication: "Double Match" should appear exactly once
        assert result.count("Double Match") == 1 + 1 + 1

        # Check total matched lines
        lines = result.strip().split("\n")
        assert len(lines) == 6  # Header + 5 unique blogs matched
