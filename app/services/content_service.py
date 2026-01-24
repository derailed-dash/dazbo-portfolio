"""
Description: Service for managing generic content pages.
Why: Handles database interactions for the 'content' collection.
How: Inherits from FirestoreService and specifies the Content model.
"""

from app.models.content import Content
from app.services.firestore_base import FirestoreService


class ContentService(FirestoreService[Content]):
    """
    Service class for interacting with the 'content' collection in Firestore.
    """

    def __init__(self, db_client):
        super().__init__(db_client, "content", Content)
