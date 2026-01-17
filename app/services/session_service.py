
from google.adk.events import Event
from google.adk.sessions import BaseSessionService, Session
from google.cloud import firestore


class FirestoreSessionService(BaseSessionService):
    def __init__(self, db: firestore.AsyncClient):
        self.db = db
        self.collection = db.collection("sessions")

    async def create_session(
        self, session_id: str, user_id: str | None = None, app_name: str | None = None, **kwargs
    ) -> Session:
        existing = await self.get_session(session_id)
        if existing:
            return existing

        session = Session(id=session_id, user_id=user_id, app_name=app_name, **kwargs)
        data = session.model_dump(mode="json")
        await self.collection.document(session_id).set(data)
        return session

    async def get_session(self, session_id: str) -> Session | None:
        doc = await self.collection.document(session_id).get()
        if doc.exists:
            data = doc.to_dict()
            return Session(**data)
        return None

    async def delete_session(self, session_id: str) -> None:
        await self.collection.document(session_id).delete()

    async def list_sessions(self, user_id: str | None = None, app_name: str | None = None) -> list[Session]:
        query = self.collection
        if user_id:
            query = query.where(filter=firestore.FieldFilter("user_id", "==", user_id))
        if app_name:
            query = query.where(filter=firestore.FieldFilter("app_name", "==", app_name))

        docs = query.stream()
        sessions = []
        async for doc in docs:
            sessions.append(Session(**doc.to_dict()))
        return sessions

    async def append_event(self, session_id: str, event: Event) -> None:
        event_data = event.model_dump(mode="json")
        doc_ref = self.collection.document(session_id)
        # Using ArrayUnion to append event
        await doc_ref.update({
            "events": firestore.ArrayUnion([event_data])
        })

    # Override internal method to update state if needed, though usually handled via update logic
    # But ADK might call this to persist state changes
    async def _update_session_state(self, session_id: str, state: dict) -> None:
         doc_ref = self.collection.document(session_id)
         await doc_ref.update({"state": state})
