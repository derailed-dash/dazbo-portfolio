"""
Description: Generic simulated Firestore service.
Why: Provides an in-memory wrapper around FirestoreService for dry runs.
How: Intercepts read/write operations and applies them to an in-memory dictionary.
"""

import uuid

from pydantic import BaseModel

from app.services.firestore_base import FirestoreService


class SimulatedFirestoreService[T: BaseModel]:
    def __init__(self, real_service: FirestoreService[T]):
        self.real_service = real_service
        self._items: dict[str, T] = {}
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            items = await self.real_service.list()
            for item in items:
                if item.id:
                    self._items[item.id] = item
            self._initialized = True

    async def create(self, item: T, item_id: str | None = None) -> T:
        await self._ensure_initialized()

        if item.id:
            item_id = item.id

        if item_id is None:
            item_id = str(uuid.uuid4())

        new_item = item.model_copy(update={"id": item_id})
        self._items[item_id] = new_item
        return new_item

    async def get(self, item_id: str) -> T | None:
        await self._ensure_initialized()
        return self._items.get(item_id)

    async def list(self) -> list[T]:
        await self._ensure_initialized()
        return list(self._items.values())

    async def update(self, item_id: str, item_data: dict) -> T | None:
        await self._ensure_initialized()
        if item_id not in self._items:
            return None

        existing_item = self._items[item_id]
        updated_item = existing_item.model_copy(update=item_data)
        self._items[item_id] = updated_item
        return updated_item

    async def delete(self, item_id: str) -> bool:
        await self._ensure_initialized()
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
