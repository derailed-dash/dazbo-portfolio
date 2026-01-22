"""
Description: Project service implementation.
Why: Handles business logic and Firestore operations for portfolio projects.
How: Extends `FirestoreService` for `Project` model and `projects` collection.
"""

import builtins

from google.cloud import firestore

from app.models.project import Project
from app.services.firestore_base import FirestoreService


class ProjectService(FirestoreService[Project]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "projects", Project)

    async def list(self) -> list[Project]:
        # Sort by created_at descending
        docs = self.collection.order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        items = []
        async for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(self.model_class(**data))
        return items

    async def get_sitemap_entries(self) -> builtins.list[dict]:
        """
        Get all project entries for sitemap (id and created_at).
        """
        results = await self.list_projection(["created_at"], order_by="created_at")

        entries = []
        for item in results:
            created_at = item.get("created_at")
            lastmod = None
            if created_at:
                # Firestore returns datetime
                if hasattr(created_at, "isoformat"):
                    lastmod = created_at.isoformat()
                else:
                    lastmod = str(created_at)

            entries.append({"id": item["id"], "lastmod": lastmod})
        return entries
