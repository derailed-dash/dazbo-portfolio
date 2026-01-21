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

    async def list(self) -> list[Experience]:
        # Sort by start_date descending
        docs = self.collection.order_by("start_date", direction=firestore.Query.DESCENDING).stream()
        items = []
        async for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(self.model_class(**data))
        return items
