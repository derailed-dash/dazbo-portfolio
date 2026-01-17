import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Firestore
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "dazbo-portfolio")
    firestore_database_id: str = os.getenv("FIRESTORE_DATABASE_ID", "(default)")

settings = Settings()
