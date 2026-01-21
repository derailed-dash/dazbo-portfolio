"""
Description: Application configuration settings.
Why: Centralizes settings from environment variables for consistent configuration across the app.
How: Uses `pydantic-settings` to load and validate environment variables.

Configuration Sources:
1. Environment Variables: In production (Cloud Run), settings are injected as environment variables.
2. .env File: For local development, settings are loaded from a `.env` file in the project root.

Usage:
    from app.config import settings
    print(settings.google_cloud_project)
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings model.

    Fields defined here are automatically populated from environment variables
    (case-insensitive) or the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env" if not os.getenv("CI") else None, env_file_encoding="utf-8", extra="ignore"
    )

    # Infrastructure
    google_cloud_project: str = "dazbo-portfolio"
    google_cloud_region: str = "europe-west1"

    # GenAI / Vertex AI Configuration
    # These are often used by the underlying Google SDKs
    google_genai_use_vertexai: bool = False
    google_cloud_location: str = "global"  # Used by Gemini model
    gemini_api_key: str | None = None  # Used when google_genai_use_vertexai is False

    # Firestore
    firestore_database_id: str = "(default)"

    # Agent
    app_name: str = "dazbo_portfolio"  # must use underscores, not hyphens
    agent_name: str = "dazbo_portfolio_chat_agent"
    log_level: str = "INFO"
    model: str = "gemini-2.5-flash"
    max_enrichment_input_chars: int = 15000
    gemini_temp: float = 0.5

    # Note that this prompt is replaced at deploy time
    dazbo_system_prompt: str = "You are Dazbo's portfolio assistant. You help visitors navigate his projects and blogs. Always provide links/URLs when mentioning specific projects or blogs."


settings = Settings()
