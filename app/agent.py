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

from app.config import settings
from app.tools.content_details import get_content_details
from app.tools.portfolio_search import search_portfolio

_, project_id = google.auth.default()

# Set defaults
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

# Ensure critical environment variables are set for the underlying SDKs (GenAI, Auth)
# based on our loaded settings.
if settings.google_cloud_project:
    os.environ["GOOGLE_CLOUD_PROJECT"] = settings.google_cloud_project
if settings.google_cloud_region:
    os.environ["GOOGLE_CLOUD_REGION"] = settings.google_cloud_region

# For Gemini model access, we use the location defined for the agent (e.g. "global" or "us-central1")
# We set this AFTER region to ensure it takes precedence in some SDK versions
if settings.google_cloud_location:
    os.environ["GOOGLE_CLOUD_LOCATION"] = settings.google_cloud_location

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(settings.google_genai_use_vertexai)
if settings.gemini_api_key:
    os.environ["GEMINI_API_KEY"] = settings.gemini_api_key


class PortfolioAgent(Agent):
    """Custom Agent subclass to fix ADK app name inference.
    The agent's class is now defined in our codebase. The ADK sees this and no longer flags
    it as a mismatch with the library's default name."""

    pass


root_agent = PortfolioAgent(
    name="root_agent",
    description="You are Dazbo's helpful assistant. You can search for content in his portfolio",
    model=Gemini(
        model=settings.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=settings.dazbo_system_prompt,
    tools=[search_portfolio, get_content_details],
)

app = App(root_agent=root_agent, name=settings.app_name)
