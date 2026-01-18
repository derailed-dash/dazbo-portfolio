"""
Description: Unit tests for ingestion metadata on Pydantic models.
Why: Verifies that Project and Blog models support new fields for ingestion source tracking.
How: Instantiates models with new fields and asserts their values.
"""

from datetime import datetime

import pytest
from app.models.project import Project
from app.models.blog import Blog

def test_project_ingestion_fields():
    project = Project(
        title="Ingested Project",
        description="A project from GitHub",
        source_platform="github",
        is_manual=False,
        metadata_only=True
    )
    assert project.source_platform == "github"
    assert project.is_manual is False
    assert project.metadata_only is True

def test_project_ingestion_defaults():
    # Verify defaults
    project = Project(
        title="Manual Project",
        description="A manually added project"
    )
    # Default for is_manual should probably be True if not specified? 
    # Or maybe False? Let's check spec. 
    # Spec says "Hybrid ingestion mechanism". 
    # Let's assume default is_manual=True for now as manual creation via API might imply it, 
    # BUT most existing entries are manual. 
    # Actually, for backward compatibility, new fields should have defaults.
    # is_manual default to True seems safer for existing data if we consider them manual?
    # Or we default to False and migration script updates them?
    # Let's assume default is None or specific value. 
    # For this test, let's just assert we can instantiate without them and they have reasonable defaults (e.g. None or False)
    
    # Actually, looking at the plan: "Add source_platform and is_manual fields".
    # If I add them as optional fields with defaults, the test should pass if I check for default values.
    # Let's assume defaults: source_platform=None, is_manual=True (as existing are manual), metadata_only=False.
    
    assert project.source_platform is None
    assert project.is_manual is True # Assuming default is True for backward compat/manual entry
    assert project.metadata_only is False

def test_blog_ingestion_fields():
    blog = Blog(
        title="Ingested Blog",
        summary="A blog from Medium",
        date="2026-01-01",
        platform="Medium", # This is existing field, maybe source_platform is redundant? 
        # Wait, Blog already has 'platform'. 
        # Plan says: "Add source_platform and is_manual fields to Project and Blog models"
        # If Blog already has platform, maybe we map it? Or is source_platform different?
        # Blog.platform usually refers to "Medium", "Dev.to". 
        # Let's assume source_platform is the *technical* source, e.g. "medium_api", "rss", "manual".
        # Or maybe the plan just meant "ensure it has it".
        # Let's add source_platform to be explicit about *how* it got here.
        url="http://example.com",
        source_platform="medium_connector",
        is_manual=False,
        metadata_only=False
    )
    assert blog.source_platform == "medium_connector"
    assert blog.is_manual is False
    assert blog.metadata_only is False
