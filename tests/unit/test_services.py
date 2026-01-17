import pytest

def test_project_service_exists():
    try:
        from app.services.project_service import ProjectService
    except ImportError:
        pytest.fail("Could not import ProjectService")

def test_blog_service_exists():
    try:
        from app.services.blog_service import BlogService
    except ImportError:
        pytest.fail("Could not import BlogService")

def test_experience_service_exists():
    try:
        from app.services.experience_service import ExperienceService
    except ImportError:
        pytest.fail("Could not import ExperienceService")
