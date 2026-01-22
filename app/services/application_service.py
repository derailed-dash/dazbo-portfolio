"""
Description: Service for managing Application entities in Firestore.
Why: Provides CRUD operations specifically for the applications collection.
How: Inherits from FirestoreService and specifies the "applications" collection.
"""

from google.cloud.firestore import AsyncClient

from app.models.application import Application
from app.services.firestore_base import FirestoreService


class ApplicationService(FirestoreService[Application]):
    def __init__(self, db: AsyncClient):
        super().__init__(db, "applications", Application)
