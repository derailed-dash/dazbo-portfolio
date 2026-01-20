"""
Description: CLI tool for ingesting portfolio resources.
Why: Orchestrates the fetching of data from various sources (GitHub, Medium, Dev.to) and saves it to Firestore.
How: Uses Typer for CLI, and service connectors for data fetching.
"""

import asyncio
import re

import typer
import yaml
from google.cloud import firestore
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from app.config import settings
from app.models.blog import Blog
from app.models.project import Project
from app.services.blog_service import BlogService
from app.services.connectors.devto_connector import DevToConnector
from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.medium_archive_connector import MediumArchiveConnector
from app.services.connectors.medium_connector import MediumConnector
from app.services.project_service import ProjectService

app = typer.Typer(help="Ingest portfolio resources from external platforms.")
console = Console()


def slugify(text: str) -> str:
    """
    Generate a slug from a string.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


async def ingest_resources(
    github_user: str | None,
    medium_user: str | None,
    medium_zip: str | None,
    devto_user: str | None,
    yaml_file: str | None,
    project_id: str,
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
                    slug = slugify(p.title)
                    await project_service.create(p, item_id=slug)
                    console.print(f"Created: {p.title} (ID: {slug})")

        except Exception as e:
            console.print(f"[bold red]Error fetching GitHub:[/bold red] {e}")

    # --- Medium (Hybrid) ---
    if medium_user or medium_zip:
        console.print("[bold blue]Processing Medium content...[/bold blue]")
        rss_blogs = []
        archive_blogs = []

        if medium_user:
            console.print(f"Fetching RSS feed for {medium_user}...")
            rss_connector = MediumConnector()
            try:
                rss_blogs = await rss_connector.fetch_posts(medium_user)
                console.print(f"Found {len(rss_blogs)} Medium posts in RSS.")
            except Exception as e:
                console.print(f"[bold red]Error fetching Medium RSS:[/bold red] {e}")

        if medium_zip:
            console.print(f"Parsing Medium archive: {medium_zip}...")
            archive_connector = MediumArchiveConnector()
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task_id = progress.add_task("Processing archive...", total=None)

                    def update_progress(processed, total, current_file):
                        progress.update(
                            task_id,
                            completed=processed,
                            total=total,
                            description=f"Processing {current_file}...",
                        )

                    archive_blogs = await archive_connector.fetch_posts(
                        medium_zip, on_progress=update_progress
                    )
                console.print(f"Found {len(archive_blogs)} Medium posts in archive.")
            except Exception as e:
                console.print(f"[bold red]Error parsing Medium archive:[/bold red] {e}")

        # Merge Logic
        # Priority: RSS for latest metadata (date, title, URL), Zip for full content
        combined_blogs: dict[str, Blog] = {}

        # First, add archive blogs (for full history)
        for b in archive_blogs:
            combined_blogs[b.url] = b

        # Then, overlay with RSS (for latest metadata)
        for b in rss_blogs:
            if b.url in combined_blogs:
                # Update existing with RSS metadata but keep archive's markdown/ai_summary
                existing = combined_blogs[b.url]
                b.markdown_content = existing.markdown_content
                b.ai_summary = existing.ai_summary
                b.is_private = existing.is_private  # Heuristic from zip is likely better
                combined_blogs[b.url] = b
            else:
                combined_blogs[b.url] = b

        # Persist to Firestore
        existing_blogs = await blog_service.list()
        existing_urls = {b.url: b.id for b in existing_blogs if b.url}

        for b in combined_blogs.values():
            # For archive-only posts, use AI summary as general summary if missing
            if not b.summary and b.ai_summary:
                b.summary = b.ai_summary[:200] + "..." if len(b.ai_summary) > 200 else b.ai_summary

            if b.url in existing_urls:
                b.id = existing_urls[b.url]
                await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                console.print(f"Updated: {b.title}")
            else:
                slug = slugify(b.title)
                await blog_service.create(b, item_id=slug)
                console.print(f"Created: {b.title} (ID: {slug})")

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
                    slug = slugify(b.title)
                    await blog_service.create(b, item_id=slug)
                    console.print(f"Created: {b.title} (ID: {slug})")

        except Exception as e:
            console.print(f"[bold red]Error fetching Dev.to:[/bold red] {e}")

    # --- Manual YAML ---
    if yaml_file:
        console.print(f"[bold blue]Processing Manual YAML: {yaml_file}...[/bold blue]")
        try:
            with open(yaml_file) as f:
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

                    # We need a map for titles too if we support that
                    existing_title_map = {}
                    ambiguous_titles = set()
                    for existing_p in existing_projects:
                        if existing_p.title in existing_title_map:
                            ambiguous_titles.add(existing_p.title)
                        existing_title_map[existing_p.title] = existing_p.id

                    match_id = None
                    if p.repo_url and p.repo_url in existing_urls:
                        match_id = existing_urls[p.repo_url]
                    elif p.title in existing_title_map:
                        if p.title in ambiguous_titles:
                            console.print(
                                f"[bold red]Error: Title '{p.title}' matches multiple existing projects. Cannot safely upsert by title. Please provide explicit 'id' or 'repo_url'. Skipping.[/bold red]"
                            )
                            continue
                        match_id = existing_title_map[p.title]

                    desired_id = None
                    if p.id:
                        desired_id = p.id
                    elif p.repo_url:
                        # try to get slug from repo url
                        desired_id = slugify(p.repo_url.split("/")[-1])
                    else:
                        console.print(
                            f"[yellow]Warning: No 'id' or 'repo_url' for manual project '{p.title}'. Using title slug as ID. This may not be stable.[/yellow]"
                        )
                        desired_id = slugify(p.title)

                    if match_id:
                        # Existing item found by repo_url or title lookup
                        # We use the EXISTING ID to update it
                        p.id = match_id
                        await project_service.update(p.id, p.model_dump(exclude={"id"}))
                        console.print(f"Updated Manual: {p.title}")
                    else:
                        # Create new with our desired ID
                        await project_service.create(p, item_id=desired_id)
                        console.print(f"Created Manual: {p.title} (ID: {desired_id})")

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

                    desired_id = None
                    if b.id:
                        desired_id = b.id
                    elif b.url:
                        # try to get slug from url
                        desired_id = slugify(b.url.split("/")[-1])
                    else:
                        console.print(
                            f"[yellow]Warning: No 'id' or 'url' for manual blog '{b.title}'. Using title slug as ID. This may not be stable.[/yellow]"
                        )
                        desired_id = slugify(b.title)

                    if b.url in existing_urls:
                        b.id = existing_urls[b.url]
                        await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                        console.print(f"Updated Manual: {b.title}")
                    else:
                        await blog_service.create(b, item_id=desired_id)
                        console.print(f"Created Manual: {b.title} (ID: {desired_id})")

        except Exception as e:
            console.print(f"[bold red]Error processing YAML:[/bold red] {e}")


@app.command()
def main(
    github_user: str = typer.Option(None, help="GitHub username"),
    medium_user: str = typer.Option(None, help="Medium username"),
    medium_zip: str = typer.Option(None, help="Path to Medium export zip file"),
    devto_user: str = typer.Option(None, help="Dev.to username"),
    yaml_file: str = typer.Option(None, help="Path to manual resources YAML file"),
    project_id: str = typer.Option(settings.google_cloud_project, help="GCP Project ID"),
):
    """
    Ingest data from configured sources.
    """
    if not project_id:
        console.print(
            "[bold red]Error: GOOGLE_CLOUD_PROJECT environment variable or --project-id option required.[/bold red]"
        )
        raise typer.Exit(code=1)

    asyncio.run(ingest_resources(github_user, medium_user, medium_zip, devto_user, yaml_file, project_id))


if __name__ == "__main__":
    app()
