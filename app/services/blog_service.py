"""
Description: Blog service implementation.
Why: Handles business logic and Firestore operations for blog posts.
How: Extends `FirestoreService` for `Blog` model and `blogs` collection.
"""

from google.cloud import firestore

from app.models.blog import Blog
from app.services.firestore_base import FirestoreService


class BlogService(FirestoreService[Blog]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "blogs", Blog)
