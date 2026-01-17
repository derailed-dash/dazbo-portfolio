from google.cloud import firestore
from app.models.blog import Blog
from app.services.firestore_base import FirestoreService

class BlogService(FirestoreService[Blog]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "blogs", Blog)
