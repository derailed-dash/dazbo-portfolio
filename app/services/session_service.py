from typing import Any

from google.adk.events import Event
from google.adk.sessions import BaseSessionService, Session
from google.adk.sessions.base_session_service import GetSessionConfig, ListSessionsResponse
from google.cloud import firestore


class FirestoreSessionService(BaseSessionService):
    def __init__(self, db: firestore.AsyncClient):
        self.db = db
        self.collection = db.collection("sessions")

    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        state: dict[str, Any] | None = None,
        session_id: str | None = None,
    ) -> Session:
        if session_id:
            existing = await self.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
            if existing:
                return existing
        else:
            # Generate an ID if not provided, though Firestore can do it too
            # We'll let ADK/Session handle it if we don't provide one?
            # Session() will generate one if id is None
            pass

        session = Session(id=session_id, user_id=user_id, app_name=app_name, state=state or {})
        data = session.model_dump(mode="json")
        await self.collection.document(session.id).set(data)
        return session

    async def get_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: GetSessionConfig | None = None,
    ) -> Session | None:
        doc = await self.collection.document(session_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data is not None and data.get("app_name") == app_name and data.get("user_id") == user_id:
                return Session(**data)
        return None

    async def delete_session(self, *, app_name: str, user_id: str, session_id: str) -> None:
        await self.collection.document(session_id).delete()

    async def list_sessions(self, *, app_name: str, user_id: str | None = None) -> ListSessionsResponse:
        query = self.collection.where(filter=firestore.FieldFilter("app_name", "==", app_name))
        if user_id:
            query = query.where(filter=firestore.FieldFilter("user_id", "==", user_id))

        docs = query.stream()
        sessions = []
        async for doc in docs:
            sessions.append(Session(**doc.to_dict()))
        return ListSessionsResponse(sessions=sessions)

    async def append_event(self, session: Session, event: Event) -> Event:
        # Call super to update session object in memory
        event = await super().append_event(session, event)
        if event.partial:
            return event

        event_data = event.model_dump(mode="json")
        doc_ref = self.collection.document(session.id)
        # Persist event and updated state to Firestore
        await doc_ref.update({"events": firestore.ArrayUnion([event_data]), "state": session.state})
        return event
