"""
Description: Firestore client singleton manager.
Why: Prevents resource leaks by ensuring a single Firestore client instance is shared across the application and tools.
How: Provides `get_client()` to access the singleton and `close_client()` for cleanup.
"""

from google.cloud import firestore

from app.config import settings

_db: firestore.AsyncClient | None = None


def get_client() -> firestore.AsyncClient:
    """
    Returns the singleton Firestore client. Initializes it if not already created.
    """
    global _db
    if _db is None:
        _db = firestore.AsyncClient(project=settings.google_cloud_project, database=settings.firestore_database_id)
    return _db


def close_client():
    """
    Closes the singleton Firestore client if it exists.
    """
    global _db
    if _db:
        _db.close()
        _db = None
