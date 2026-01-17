from google.cloud import firestore

from app.models.project import Project
from app.services.firestore_base import FirestoreService


class ProjectService(FirestoreService[Project]):
    def __init__(self, db: firestore.AsyncClient):
        super().__init__(db, "projects", Project)
