"""
Description: AI service for content enrichment.
Why: Provides utility methods for interacting with Gemini, such as generating summaries.
How: Uses the google-genai SDK to call Gemini models.
"""

from google.genai import Client, types

from app.config import settings


class ContentEnrichmentService:
    def __init__(self):
        # Configure client based on settings
        if settings.google_genai_use_vertexai:
            self.client = Client(
                vertexai=True, project=settings.google_cloud_project, location=settings.google_cloud_location
            )
        else:
            self.client = Client(api_key=settings.gemini_api_key)

        self.model = settings.model

    async def generate_summary(self, text: str) -> str:
        """
        Generates a concise summary of the provided text using Gemini.
        """
        prompt = (
            "You are a professional technical writer. Summarise the following blog post content into "
            "a concise paragraph (max 200 words). Focus on the key takeaways and technical value.\n\n"
            f"Content:\n{text}"
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=300,
            ),
        )

        return response.text.strip()
