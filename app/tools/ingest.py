"""
Description: CLI tool for ingesting portfolio resources.
Why: Orchestrates the fetching of data from various sources (GitHub, Medium, Dev.to) and saves it to Firestore.
How: Uses Typer for CLI, and service connectors for data fetching.
"""

import asyncio
import typer
from google.cloud import firestore
from rich.console import Console

from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.medium_connector import MediumConnector
from app.services.connectors.devto_connector import DevToConnector
from app.services.project_service import ProjectService
from app.services.blog_service import BlogService
from app.config import settings

app = typer.Typer(help="Ingest portfolio resources from external platforms.")
console = Console()

async def ingest_resources(
    github_user: str | None,
    medium_user: str | None,
    devto_user: str | None,
    project_id: str
):
    """
    Async logic for ingestion.
    """
    db = firestore.AsyncClient(project=project_id)
    project_service = ProjectService(db)
    blog_service = BlogService(db)
    
    # --- GitHub ---
    if github_user:
        console.print(f"[bold blue]Fetching GitHub repos for {github_user}...[/bold blue]")
        connector = GitHubConnector()
        try:
            projects = await connector.fetch_repositories(github_user)
            console.print(f"Found {len(projects)} repositories.")
            
            # Simple idempotency: check if exists by some unique key?
            # For now, we'll iterate and update/create.
            # Ideally we check by 'repo_url' or similar unique field.
            # But generic service 'list' returns all.
            # Let's simple-create for now, assuming logic inside service or ID generation handles duplicates?
            # Actually, ProjectService uses ID. If we don't provide ID, it creates new.
            # We should probably query by 'source_platform' and 'repo_url' to find existing.
            # But the service doesn't have custom query yet.
            # Plan says: "Add logic to ensure idempotency (prevent duplicates in Firestore)"
            
            # Implementation choice: Retrieve all projects first (naive)
            # or implement a check in loop.
            # Let's fetch all existing projects first to map URL -> ID
            existing_projects = await project_service.list()
            existing_urls = {p.repo_url: p.id for p in existing_projects if p.repo_url}
            
            for p in projects:
                if p.repo_url in existing_urls:
                    # Update existing
                    p.id = existing_urls[p.repo_url]
                    # We need to convert p to dict for update, but update takes id and dict
                    # Also, we might not want to overwrite EVERYTHING if manual edits exist?
                    # For now, full sync: overwrite fields.
                    await project_service.update(p.id, p.model_dump(exclude={"id"}))
                    console.print(f"Updated: {p.title}")
                else:
                    # Create new
                    await project_service.create(p)
                    console.print(f"Created: {p.title}")
                    
        except Exception as e:
            console.print(f"[bold red]Error fetching GitHub:[/bold red] {e}")

    # --- Medium ---
    if medium_user:
        console.print(f"[bold blue]Fetching Medium posts for {medium_user}...[/bold blue]")
        connector = MediumConnector()
        try:
            blogs = await connector.fetch_posts(medium_user)
            console.print(f"Found {len(blogs)} Medium posts.")
            
            existing_blogs = await blog_service.list()
            existing_urls = {b.url: b.id for b in existing_blogs if b.url}
            
            for b in blogs:
                if b.url in existing_urls:
                    b.id = existing_urls[b.url]
                    await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                    console.print(f"Updated: {b.title}")
                else:
                    await blog_service.create(b)
                    console.print(f"Created: {b.title}")

        except Exception as e:
            console.print(f"[bold red]Error fetching Medium:[/bold red] {e}")

    # --- Dev.to ---
    if devto_user:
        console.print(f"[bold blue]Fetching Dev.to posts for {devto_user}...[/bold blue]")
        connector = DevToConnector()
        try:
            blogs = await connector.fetch_posts(devto_user)
            console.print(f"Found {len(blogs)} Dev.to posts.")
            
            existing_blogs = await blog_service.list()
            existing_urls = {b.url: b.id for b in existing_blogs if b.url}
            
            for b in blogs:
                if b.url in existing_urls:
                    b.id = existing_urls[b.url]
                    await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                    console.print(f"Updated: {b.title}")
                else:
                    await blog_service.create(b)
                    console.print(f"Created: {b.title}")
                    
        except Exception as e:
            console.print(f"[bold red]Error fetching Dev.to:[/bold red] {e}")

@app.command()
def main(
    github_user: str = typer.Option(None, help="GitHub username"),
    medium_user: str = typer.Option(None, help="Medium username"),
    devto_user: str = typer.Option(None, help="Dev.to username"),
    project_id: str = typer.Option(settings.google_cloud_project, help="GCP Project ID")
):
    """
    Ingest data from configured sources.
    """
    if not project_id:
        console.print("[bold red]Error: GOOGLE_CLOUD_PROJECT environment variable or --project-id option required.[/bold red]")
        raise typer.Exit(code=1)

    asyncio.run(ingest_resources(github_user, medium_user, devto_user, project_id))

if __name__ == "__main__":
    app()
