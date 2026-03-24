"""
Description: Service for managing Video data in Firestore.
Why: Provides specific methods for interacting with the 'videos' collection.
How: Inherits from the generic FirestoreService.
"""

from google.cloud import firestore

from app.models.video import Video
from app.services.firestore_base import FirestoreService


class VideoService(FirestoreService[Video]):
    """
    Service for managing video records in Firestore.
    """
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "videos", Video)
