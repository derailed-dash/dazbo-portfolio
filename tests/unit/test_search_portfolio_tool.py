import pytest
from unittest.mock import AsyncMock, patch
from app.models.project import Project
from app.models.blog import Blog

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
            featured=False
        ),
        Project(
            id="proj2", 
            title="React Dashboard", 
            description="A dashboard built with React", 
            tags=["react", "typescript"],
            repo_url="http://github.com/user/dashboard",
            demo_url=None,
            image_url=None,
            featured=True
        )
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
            tags=["python", "learning"]
        ),
        Blog(
            id="blog2", 
            title="Advanced TypeScript", 
            summary="Deep dive into TS", 
            url="http://dev.to/post2", 
            date="2025-01-02", 
            platform="Dev.to",
            tags=["typescript", "web"]
        )
    ]

@pytest.mark.asyncio
async def test_search_portfolio_by_tag(mock_projects, mock_blogs):
    with patch("app.tools.portfolio_search.ProjectService") as MockProjectService, \
         patch("app.tools.portfolio_search.BlogService") as MockBlogService, \
         patch("app.tools.portfolio_search.firestore.AsyncClient"):
        
        # Setup mocks
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service
        
        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        # Test searching for "python"
        result = await search_portfolio("python")
        
        assert "Python Automation" in result
        assert "Learning Python" in result
        assert "React Dashboard" not in result

@pytest.mark.asyncio
async def test_search_portfolio_by_text(mock_projects, mock_blogs):
    with patch("app.tools.portfolio_search.ProjectService") as MockProjectService, \
         patch("app.tools.portfolio_search.BlogService") as MockBlogService, \
         patch("app.tools.portfolio_search.firestore.AsyncClient"):
        
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service
        
        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        # Test searching for "dashboard" (in title of project)
        result = await search_portfolio("Dashboard")
        
        assert "React Dashboard" in result
        assert "Python Automation" not in result

@pytest.mark.asyncio
async def test_search_portfolio_no_results(mock_projects, mock_blogs):
    with patch("app.tools.portfolio_search.ProjectService") as MockProjectService, \
         patch("app.tools.portfolio_search.BlogService") as MockBlogService, \
         patch("app.tools.portfolio_search.firestore.AsyncClient"):
        
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service
        
        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        result = await search_portfolio("java")
        
        assert "No projects or blogs found" in result

@pytest.mark.asyncio
async def test_search_portfolio_case_insensitive(mock_projects, mock_blogs):
    with patch("app.tools.portfolio_search.ProjectService") as MockProjectService, \
         patch("app.tools.portfolio_search.BlogService") as MockBlogService, \
         patch("app.tools.portfolio_search.firestore.AsyncClient"):
        
        proj_service = AsyncMock()
        proj_service.list.return_value = mock_projects
        MockProjectService.return_value = proj_service
        
        blog_service = AsyncMock()
        blog_service.list.return_value = mock_blogs
        MockBlogService.return_value = blog_service

        result = await search_portfolio("PYTHON")
        
        assert "Python Automation" in result
