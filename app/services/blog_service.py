"""
Description: Blog service implementation.
Why: Handles business logic and Firestore operations for blog posts.
How: Extends `FirestoreService` for `Blog` model and `blogs` collection.
"""

from google.cloud import firestore

from app.config import settings
from app.models.blog import Blog
from app.services.firestore_base import FirestoreService


class BlogService(FirestoreService[Blog]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "blogs", Blog)

    async def list(self) -> list[Blog]:
        # Sort by date descending
        docs = self.collection.order_by("date", direction=firestore.Query.DESCENDING).stream()
        items = []
        async for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            
            # Enrich with author profile URL based on platform
            platform = (data.get("platform") or "").lower()
            if "medium" in platform:
                data["author_url"] = settings.medium_profile
            elif "dev.to" in platform:
                data["author_url"] = settings.devto_profile

            items.append(self.model_class(**data))
        return items
