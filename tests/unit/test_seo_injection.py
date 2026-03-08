"""
Description: Unit tests for SEO Injection API and HTML serving.
Why: Verifies that the /api/seo endpoint and HTML injection work correctly.
How: Uses FastAPI TestClient.
"""

from fastapi.testclient import TestClient

from app.fast_api_app import app

client = TestClient(app)

def test_api_seo_home():
    """Test the /api/seo endpoint for the root path."""
    response = client.get("/api/seo?path=/")
    # This should fail initially in TDD
    assert response.status_code == 200
    data = response.json()
    assert "head_tags" in data
    assert '<title>Darren \'Dazbo\' Lester | Enterprise Cloud Architect | Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist</title>' in data["head_tags"]
    assert 'rel="canonical"' in data["head_tags"]
    assert 'property="og:title"' in data["head_tags"]


def test_api_seo_about():
    """Test the /api/seo endpoint for the about path."""
    response = client.get("/api/seo?path=/about")
    # This should fail initially in TDD
    assert response.status_code == 200
    data = response.json()
    assert "head_tags" in data
    assert '<title>About Darren Lester | Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist</title>' in data["head_tags"]
    assert 'rel="canonical"' in data["head_tags"]
    assert 'property="og:title"' in data["head_tags"]


def test_serve_spa_injection_home():
    """Test that the served HTML contains injected SEO tags instead of placeholders."""
    # Assuming frontend/dist/index.html is being served
    response = client.get("/")
    assert response.status_code == 200
    html = response.text

    # This should fail initially because the injection logic isn't there
    # and the placeholders aren't there or replaced
    assert '<title>Darren \'Dazbo\' Lester | Enterprise Cloud Architect | Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist</title>' in html
    assert 'property="og:title"' in html
    assert "<!-- __SEO_TAGS__ -->" not in html


def test_serve_spa_injection_about():
    """Test that the served HTML contains injected SEO tags for about page."""
    # Assuming frontend/dist/index.html is being served
    response = client.get("/about")
    assert response.status_code == 200
    html = response.text

    # This should fail initially
    assert '<title>About Darren Lester | Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist</title>' in html
    assert 'property="og:title"' in html
    assert "<!-- __SEO_TAGS__ -->" not in html

