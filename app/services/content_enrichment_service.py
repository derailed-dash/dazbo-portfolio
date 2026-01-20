"""
Description: AI service for content extraction and summarisation.
Why: Provides utility methods for interacting with Gemini, such as generating summaries.
How: Uses the google-genai SDK to call Gemini models.
"""

import json

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

    async def enrich_content(self, text: str) -> dict:
        """
        Generates a summary and tags for the provided text.
        Returns: {"summary": str, "tags": list[str]}
        """
        # Limit input text to avoid overwhelming the model or hitting response limits
        # 15000 chars is roughly 3000-4000 tokens, plenty for a summary.
        truncated_text = text[:15000]

        prompt = (
            "You are a professional technical writer. Analyze the following blog post content.\n"
            "1. Generate a comprehensive summary (max 225 words) focusing on key technical takeaways.\n"
            "2. Propose 5 relevant technical tags.\n\n"
            "Return the result as a valid JSON object with keys 'summary' and 'tags'.\n"
            'Example format: {"summary": "Actual summary text here", "tags": ["tag1", "tag2"]}\n\n'
            f"Content:\n{truncated_text}"
        )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2048,
                response_mime_type="application/json",
            ),
        )

        if not response.text:
            return {"summary": "", "tags": []}

        try:
            # Clean up potential markdown wrappers or extra whitespace
            cleaned_text = response.text.strip()
            if cleaned_text.startswith("```"):
                import re

                cleaned_text = re.sub(r"^```(?:json)?\n", "", cleaned_text)
                cleaned_text = re.sub(r"\n```$", "", cleaned_text)

            data = json.loads(cleaned_text)

            # Ensure summary is a string and not a nested dict (sometimes models hallucinate structure)
            summary = data.get("summary", "")
            if isinstance(summary, dict):
                summary = summary.get("summary", str(summary))

            tags = data.get("tags", [])
            if not isinstance(tags, list):
                tags = [str(tags)] if tags else []

            return {"summary": str(summary), "tags": [str(t) for t in tags]}

        except (json.JSONDecodeError, Exception) as e:
            # Fallback if model doesn't return valid JSON
            print(f"Error parsing AI enrichment JSON: {e}")
            return {"summary": response.text.strip(), "tags": []}
