from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from app.dependencies import get_blog_service, get_project_service


def test_sitemap_xml():
    from app.fast_api_app import app

    # Mock BlogService
    mock_blog_service = MagicMock()
    mock_blog_service.get_sitemap_entries = AsyncMock(
        return_value=[
            {"id": "blog-1", "lastmod": "2023-01-01"},
            {"id": "blog-2", "lastmod": "2023-01-02"},
        ]
    )

    # Mock ProjectService
    mock_project_service = MagicMock()
    mock_project_service.get_sitemap_entries = AsyncMock(
        return_value=[
            {"id": "proj-1", "lastmod": "2023-02-01"},
        ]
    )

    app.dependency_overrides[get_blog_service] = lambda: mock_blog_service
    app.dependency_overrides[get_project_service] = lambda: mock_project_service

    try:
        with TestClient(app) as client:
            response = client.get("/sitemap.xml")
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/xml"

            content = response.text
            assert "<?xml" in content
            assert "<urlset" in content
            # Check for static pages
            assert "<loc>https://darrenlester.net/</loc>" in content

            # Check for dynamic blogs
            assert "<loc>https://darrenlester.net/details/blog-1</loc>" in content
            assert "<lastmod>2023-01-01</lastmod>" in content

            # Check for dynamic projects
            assert "<loc>https://darrenlester.net/details/proj-1</loc>" in content
            assert "<lastmod>2023-02-01</lastmod>" in content

    finally:
        app.dependency_overrides.clear()
