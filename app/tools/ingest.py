"""
Description: CLI tool for ingesting portfolio resources.
Why: Orchestrates the fetching of data from various sources (GitHub, Medium, Dev.to) and saves it to Firestore.
How: Uses Typer for CLI, and service connectors for data fetching.
"""

import asyncio
import typer
import yaml
from google.cloud import firestore
from rich.console import Console

from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.medium_connector import MediumConnector
from app.services.connectors.devto_connector import DevToConnector
from app.services.project_service import ProjectService
from app.services.blog_service import BlogService
from app.models.project import Project
from app.models.blog import Blog
from app.config import settings

app = typer.Typer(help="Ingest portfolio resources from external platforms.")
console = Console()

async def ingest_resources(
    github_user: str | None,
    medium_user: str | None,
    devto_user: str | None,
    yaml_file: str | None,
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
            
            existing_projects = await project_service.list()
            existing_urls = {p.repo_url: p.id for p in existing_projects if p.repo_url}
            
            for p in projects:
                if p.repo_url in existing_urls:
                    p.id = existing_urls[p.repo_url]
                    await project_service.update(p.id, p.model_dump(exclude={"id"}))
                    console.print(f"Updated: {p.title}")
                else:
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

    # --- Manual YAML ---
    if yaml_file:
        console.print(f"[bold blue]Processing Manual YAML: {yaml_file}...[/bold blue]")
        try:
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
            
            # Process Projects
            manual_projects = data.get("projects", [])
            if manual_projects:
                console.print(f"Found {len(manual_projects)} manual projects.")
                existing_projects = await project_service.list()
                existing_urls = {p.repo_url: p.id for p in existing_projects if p.repo_url}
                
                for proj_data in manual_projects:
                    # Enforce manual flags
                    proj_data["is_manual"] = True
                    proj_data["source_platform"] = "manual"
                    
                    try:
                        p = Project(**proj_data)
                    except Exception as validation_err:
                        console.print(f"[red]Validation Error for project {proj_data.get('title')}: {validation_err}[/red]")
                        continue

                    # Upsert logic based on repo_url if present, else title?
                    # Ideally we have a stable key. If repo_url is missing (e.g. private/local), use title?
                    # Let's fallback to title if repo_url is None
                    key = p.repo_url if p.repo_url else p.title
                    
                    # We need a map for titles too if we support that
                    existing_titles = {p.title: p.id for p in existing_projects}
                    
                    match_id = None
                    if p.repo_url and p.repo_url in existing_urls:
                        match_id = existing_urls[p.repo_url]
                    elif p.title in existing_titles:
                        match_id = existing_titles[p.title]

                    if match_id:
                        p.id = match_id
                        await project_service.update(p.id, p.model_dump(exclude={"id"}))
                        console.print(f"Updated Manual: {p.title}")
                    else:
                        await project_service.create(p)
                        console.print(f"Created Manual: {p.title}")

            # Process Blogs
            manual_blogs = data.get("blogs", [])
            if manual_blogs:
                console.print(f"Found {len(manual_blogs)} manual blogs.")
                existing_blogs = await blog_service.list()
                existing_urls = {b.url: b.id for b in existing_blogs if b.url}
                
                for blog_data in manual_blogs:
                    blog_data["is_manual"] = True
                    blog_data["source_platform"] = "manual"
                    
                    try:
                        b = Blog(**blog_data)
                    except Exception as validation_err:
                        console.print(f"[red]Validation Error for blog {blog_data.get('title')}: {validation_err}[/red]")
                        continue
                        
                    if b.url in existing_urls:
                        b.id = existing_urls[b.url]
                        await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                        console.print(f"Updated Manual: {b.title}")
                    else:
                        await blog_service.create(b)
                        console.print(f"Created Manual: {b.title}")

        except Exception as e:
             console.print(f"[bold red]Error processing YAML:[/bold red] {e}")


@app.command()
def main(
    github_user: str = typer.Option(None, help="GitHub username"),
    medium_user: str = typer.Option(None, help="Medium username"),
    devto_user: str = typer.Option(None, help="Dev.to username"),
    yaml_file: str = typer.Option(None, help="Path to manual resources YAML file"),
    project_id: str = typer.Option(settings.google_cloud_project, help="GCP Project ID")
):
    """
    Ingest data from configured sources.
    """
    if not project_id:
        console.print("[bold red]Error: GOOGLE_CLOUD_PROJECT environment variable or --project-id option required.[/bold red]")
        raise typer.Exit(code=1)

    asyncio.run(ingest_resources(github_user, medium_user, devto_user, yaml_file, project_id))

    """
    Ingest data from configured sources.
    """
    if not project_id:
        console.print("[bold red]Error: GOOGLE_CLOUD_PROJECT environment variable or --project-id option required.[/bold red]")
        raise typer.Exit(code=1)

    asyncio.run(ingest_resources(github_user, medium_user, devto_user, project_id))

if __name__ == "__main__":
    app()
