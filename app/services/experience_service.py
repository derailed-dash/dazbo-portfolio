"""
Description: Experience service implementation.
Why: Handles business logic and Firestore operations for work experience entries.
How: Extends `FirestoreService` for `Experience` model and `experience` collection.
"""

from google.cloud import firestore

from app.models.experience import Experience
from app.services.firestore_base import FirestoreService


class ExperienceService(FirestoreService[Experience]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "experience", Experience)
