"""
Description: Unit tests for SEO Injection API and HTML serving.
Why: Verifies that the /api/seo endpoint and HTML injection work correctly.
How: Uses FastAPI TestClient.
"""

from unittest.mock import mock_open, patch

from fastapi.testclient import TestClient

from app.fast_api_app import app

client = TestClient(app)

MOCK_INDEX_HTML = '<!doctype html><html lang="en"><head><!-- __SEO_TAGS__ --></head><body><div id="root"></div></body></html>'

def test_api_seo_home():
    """Test the /api/seo endpoint for the root path."""
    response = client.get("/api/seo?path=/")
    assert response.status_code == 200
    data = response.json()
    assert "head_tags" in data
    assert "title" in data
    assert data["title"] == 'Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist'
    assert '<title>Darren &quot;Dazbo&quot; Lester - Enterprise Cloud Architect and Google Evangelist</title>' in data["head_tags"]
    assert 'rel="canonical"' in data["head_tags"]
    assert 'property="og:title"' in data["head_tags"]


def test_api_seo_about():
    """Test the /api/seo endpoint for the about path."""
    response = client.get("/api/seo?path=/about")
    assert response.status_code == 200
    data = response.json()
    assert "head_tags" in data
    assert "title" in data
    assert data["title"] == 'About Darren Lester | Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist'
    assert '<title>About Darren Lester | Darren &quot;Dazbo&quot; Lester - Enterprise Cloud Architect and Google Evangelist</title>' in data["head_tags"]
    assert 'rel="canonical"' in data["head_tags"]
    assert 'property="og:title"' in data["head_tags"]


def test_serve_spa_injection_home():
    """Test that the served HTML contains injected SEO tags instead of placeholders."""
    # We mock isfile and open to avoid needing the real frontend/dist/index.html
    def mock_isfile(path):
        if path.endswith("index.html"):
            return True
        return False

    with patch("os.path.isfile", side_effect=mock_isfile), \
         patch("builtins.open", mock_open(read_data=MOCK_INDEX_HTML)):
        response = client.get("/")
        assert response.status_code == 200
        html = response.text
        assert '<title>Darren &quot;Dazbo&quot; Lester - Enterprise Cloud Architect and Google Evangelist</title>' in html
        assert 'property="og:title"' in html
        assert "<!-- __SEO_TAGS__ -->" not in html


def test_serve_spa_injection_about():
    """Test that the served HTML contains injected SEO tags for about page."""
    # We mock isfile and open to avoid needing the real frontend/dist/index.html
    def mock_isfile(path):
        if path.endswith("index.html"):
            return True
        return False

    with patch("os.path.isfile", side_effect=mock_isfile), \
         patch("builtins.open", mock_open(read_data=MOCK_INDEX_HTML)):
        response = client.get("/about")
        assert response.status_code == 200
        html = response.text
        assert '<title>About Darren Lester | Darren &quot;Dazbo&quot; Lester - Enterprise Cloud Architect and Google Evangelist</title>' in html
        assert 'property="og:title"' in html
        assert "<!-- __SEO_TAGS__ -->" not in html


def test_api_seo_xss_protection():
    """Test that the /api/seo endpoint escapes malicious paths to prevent XSS."""
    malicious_path = "</title><script>alert(1)</script>"
    response = client.get(f"/api/seo?path={malicious_path}")
    assert response.status_code == 200
    data = response.json()

    # The title in head_tags should be escaped (and handle default title casing)
    assert "&lt;/Title&gt;&lt;Script&gt;Alert(1)&lt;/Script&gt;" in data["head_tags"]
    assert "<script>alert(1)</script>" not in data["head_tags"]

    # The canonical URL should also be escaped
    # Use BASE_URL from settings/env
    from app.config import settings
    base_url = settings.base_url or "http://testserver"
    assert f'rel="canonical" href="{base_url}/&lt;/title&gt;&lt;script&gt;alert(1)&lt;/script&gt;"' in data["head_tags"]

