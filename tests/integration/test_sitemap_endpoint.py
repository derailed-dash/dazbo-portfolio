from fastapi.testclient import TestClient


def test_sitemap_xml():
    # Mock settings.base_url for the test since CI might have it empty
    from app.config import settings
    from app.fast_api_app import app

    original_base_url = settings.base_url
    settings.base_url = "https://darrenlester.net"

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

            # Verify dynamic details are NOT present
            assert "/details/" not in content

    finally:
        settings.base_url = original_base_url
