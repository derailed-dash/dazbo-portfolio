from typing import Generic, TypeVar

from google.cloud import firestore
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class FirestoreService(Generic[T]):
    def __init__(self, db: firestore.AsyncClient, collection_name: str, model_class: type[T]):
        self.db = db
        self.collection = db.collection(collection_name)
        self.model_class = model_class

    async def create(self, item: T, item_id: str | None = None) -> T:
        data = item.model_dump(mode="json", exclude={"id"}) # Exclude ID from payload, we use doc ID
        # If item has explicit ID set, use it.
        if item.id:
            item_id = item.id

        if item_id:
            doc_ref = self.collection.document(item_id)
            await doc_ref.set(data)
        else:
            update_time, doc_ref = await self.collection.add(data)
            item_id = doc_ref.id

        # Return a copy with the ID set
        return item.model_copy(update={"id": item_id})

    async def get(self, item_id: str) -> T | None:
        doc_ref = self.collection.document(item_id)
        doc = await doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return self.model_class(**data)
        return None

    async def list(self) -> list[T]:
        # Simple list all, pagination can be added later
        docs = self.collection.stream()
        items = []
        async for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(self.model_class(**data))
        return items

    async def update(self, item_id: str, item_data: dict) -> T | None:
        doc_ref = self.collection.document(item_id)
        # Using update() which fails if doc doesn't exist
        # Or set(..., merge=True) which creates if not exists
        # We likely want update semantics
        try:
            await doc_ref.update(item_data)
            # Fetch updated to return full object
            return await self.get(item_id)
        except Exception:
            # Handle not found or other errors
            return None

    async def delete(self, item_id: str) -> bool:
        doc_ref = self.collection.document(item_id)
        await doc_ref.delete()
        return True
