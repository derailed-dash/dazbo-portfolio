"""
Description: Unit tests for Service existence.
Why: Verifies that service classes can be imported, ensuring no circular dependency or syntax errors.
How: Simple import checks.
"""

import pytest


def test_project_service_exists():
    try:
        from app.services.project_service import ProjectService  # noqa: F401

    except ImportError:
        pytest.fail("Could not import ProjectService")


def test_blog_service_exists():
    try:
        from app.services.blog_service import BlogService  # noqa: F401

    except ImportError:
        pytest.fail("Could not import BlogService")


def test_experience_service_exists():
    try:
        from app.services.experience_service import ExperienceService  # noqa: F401

    except ImportError:
        pytest.fail("Could not import ExperienceService")
