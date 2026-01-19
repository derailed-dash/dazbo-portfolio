"""
Description: Main agent logic and configuration.
Why: Defines the core Gemini agent, its tools, and the ADK application wrapper.
How: Initializes `google.adk.agents.Agent` with Gemini model and tools. Wraps it in `google.adk.apps.App`.
"""

import os

import google.auth
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools.portfolio_search import search_portfolio
from app.tools.content_details import get_content_details
from app.config import settings

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Ensure critical environment variables are set for the underlying SDKs (GenAI, Auth)
# based on our loaded settings.
if settings.google_cloud_project:
    os.environ["GOOGLE_CLOUD_PROJECT"] = settings.google_cloud_project
if settings.google_cloud_location:
    os.environ["GOOGLE_CLOUD_LOCATION"] = settings.google_cloud_location
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(settings.google_genai_use_vertexai)
if settings.gemini_api_key:
    os.environ["GEMINI_API_KEY"] = settings.gemini_api_key

_, project_id = google.auth.default()

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=settings.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=settings.dazbo_system_prompt,
    tools=[search_portfolio, get_content_details],
)

app = App(root_agent=root_agent, name="app")
