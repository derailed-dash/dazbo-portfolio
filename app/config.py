"""
Description: Application configuration settings.
Why: Centralizes settings from environment variables for consistent configuration across the app.
How: Uses `pydantic-settings` to load and validate environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Infrastructure
    google_cloud_project: str = "dazbo-portfolio"
    google_cloud_location: str = "europe-west1"

    # Firestore
    firestore_database_id: str = "(default)"

    # Agent
    agent_name: str = "dazbo-portfolio"
    log_level: str = "INFO"
    model: str = "gemini-3-flash-preview"
    google_genai_use_vertexai: bool = False
    gemini_api_key: str | None = None


settings = Settings()
