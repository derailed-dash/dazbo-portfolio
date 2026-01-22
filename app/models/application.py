"""
Description: Application data model.
Why: Defines the schema for curated applications in the portfolio.
How: Reuses the structure of Project but is stored in a separate collection.
"""

from app.models.project import Project


class Application(Project):
    """
    Represents a curated application.
    Currently inherits all fields from Project.
    """
    pass
