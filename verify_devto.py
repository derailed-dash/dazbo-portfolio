import asyncio
import os
import sys

# Add project root to path so imports work
sys.path.append(os.getcwd())

from app.services.connectors.devto_connector import DevToConnector
from app.services.content_enrichment_service import ContentEnrichmentService

async def main():
    print("Initializing services...")
    try:
        enrichment_service = ContentEnrichmentService()
        connector = DevToConnector()
        
        print("Fetching posts with enrichment for 'deraileddash'...")
        # Only process 1 post to save tokens/time if possible, but fetch_posts fetches all.
        # We'll just print the first one that has enrichment.
        blogs = await connector.fetch_posts("deraileddash", enrichment_service=enrichment_service, limit=1)
        
        if blogs:
            print(f"Fetched {len(blogs)} blogs.")
            blog = blogs[0]
            print(f"\n--- Blog: {blog.title} ---")
            print(f"AI Summary: {blog.ai_summary}")
            print(f"Tags: {blog.tags}")
            print(f"Markdown Content Length: {len(blog.markdown_content) if blog.markdown_content else 0}")
        else:
            print("No blogs found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

