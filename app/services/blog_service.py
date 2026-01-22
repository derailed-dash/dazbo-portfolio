"""
Description: Blog service implementation.
Why: Handles business logic and Firestore operations for blog posts.
How: Extends `FirestoreService` for `Blog` model and `blogs` collection.
"""

import builtins

from google.cloud import firestore

from app.config import settings
from app.models.blog import Blog
from app.services.firestore_base import FirestoreService


class BlogService(FirestoreService[Blog]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "blogs", Blog)

    def _enrich_blog_data(self, data: dict) -> dict:
        """Enrich blog data with computed fields."""
        # Enrich with author profile URL based on platform
        platform = (data.get("platform") or "").lower()
        if "medium" in platform:
            data["author_url"] = settings.medium_profile
        elif "dev.to" in platform:
            data["author_url"] = settings.devto_profile
        return data

    async def get(self, item_id: str) -> Blog | None:
        doc_ref = self.collection.document(item_id)
        doc = await doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            data = self._enrich_blog_data(data)
            return self.model_class(**data)
        return None

    async def list(self) -> list[Blog]:
        # Sort by date descending
        docs = self.collection.order_by("date", direction=firestore.Query.DESCENDING).stream()
        items = []
        async for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            data = self._enrich_blog_data(data)
            items.append(self.model_class(**data))
        return items

    async def get_sitemap_entries(self) -> builtins.list[dict]:
        """
        Get all blog entries for sitemap (id and date).
        Only returns public blogs (is_private=False).
        """
        # Note: We can't filter by is_private in list_projection easily if we didn't implement filtering there.
        # But we can select is_private and filter in python.
        # Ideally we should push filter to DB.
        # But list_projection doesn't support where() yet.
        # Given small dataset, fetching is_private is fine.

        # Projection: id, date, is_private
        results = await self.list_projection(["date", "is_private"], order_by="date")

        # Filter and map
        entries = []
        for item in results:
            if not item.get("is_private", False):
                entries.append({"id": item["id"], "lastmod": item["date"]})
        return entries
