"""
Description: Project service implementation.
Why: Handles business logic and Firestore operations for portfolio projects.
How: Extends `FirestoreService` for `Project` model and `projects` collection.
"""

from google.cloud import firestore

from app.models.project import Project
from app.services.firestore_base import FirestoreService


class ProjectService(FirestoreService[Project]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "projects", Project)
