from datetime import UTC, datetime

import pytest


def test_project_model():
    try:
        from app.models.project import Project
    except ImportError:
        pytest.fail("Could not import Project model")

    project = Project(
        id="p1",
        title="Test Project",
        description="A test project",
        tags=["python", "ai"],
        featured=True,
        created_at=datetime.now(UTC)
    )
    assert project.title == "Test Project"
    assert project.tags == ["python", "ai"]

def test_blog_model():
    try:
        from app.models.blog import Blog
    except ImportError:
        pytest.fail("Could not import Blog model")

    blog = Blog(
        id="b1",
        title="Test Blog",
        summary="A test blog summary",
        date="2026-01-17",
        platform="Medium",
        url="https://medium.com/test",
        created_at=datetime.now(UTC)
    )
    assert blog.title == "Test Blog"

def test_experience_model():
    try:
        from app.models.experience import Experience
    except ImportError:
        pytest.fail("Could not import Experience model")

    experience = Experience(
        id="e1",
        company="Google",
        role="Engineer",
        duration="2020 - Present",
        description="Working on cloud stuff",
        skills=["Go", "Python"],
        order=1
    )
    assert experience.company == "Google"
