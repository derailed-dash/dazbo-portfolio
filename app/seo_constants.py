"""
Description: SEO constants and structured data mapping.
Why: Externalizes the metadata definitions to keep the main application routing file clean.
How: Provides functions that construct predefined schema.org dictionaries.
"""


def get_person_schema(base_url: str) -> dict:
    """Returns the Person schema for Darren Lester."""
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": "https://darrenlester.net/#person",
        "name": "Darren Lester",
        "alternateName": "Dazbo",
        "jobTitle": "Enterprise Cloud Architect",
        "url": base_url,
        "sameAs": [
            "https://github.com/derailed-dash",
            "https://www.linkedin.com/in/darren-lester-architect/",
            "https://medium.com/@derailed.dash",
            "https://dev.to/deraileddash",
            "https://sessionize.com/dazbo/",
        ],
        "knowsAbout": [
            "Google Cloud",
            "Generative AI",
            "Model Context Protocol",
            "Architecture",
            "Cloud Architecture",
            "ADK",
            "Agent Development Kit",
            "Agentic AI",
            "Gemini",
            "Gemini CLI",
            "Antigravity",
            "MCP",
            "Agent skills",
        ],
        "description": "Enterprise Cloud Architect, Google Developer Expert (GDE), and Google AI Champion, specializing in Google Cloud, agentic AI, cloud architecture and cloud strategy. Note: Not to be confused with the frontend engineer or other individuals of the same name.",
    }
