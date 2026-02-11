"""
Description: CLI tool for ingesting portfolio resources.
Why: Orchestrates the fetching of data from various sources (GitHub, Medium, Dev.to) and saves it to Firestore.
How: Uses Typer for CLI, and service connectors for data fetching.
"""

import asyncio
import os
import re
import zipfile
from datetime import UTC, datetime

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
from app.models.application import Application
from app.models.blog import Blog
from app.models.content import Content
from app.models.project import Project
from app.services.application_service import ApplicationService
from app.services.blog_service import BlogService
from app.services.connectors.devto_connector import DevToConnector
from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.medium_archive_connector import MediumArchiveConnector
from app.services.connectors.medium_connector import MediumConnector
from app.services.content_enrichment_service import ContentEnrichmentService
from app.services.content_service import ContentService
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


def normalize_url(url: str | None) -> str:
    """
    Normalize a URL by stripping query parameters and trailing slashes.
    """
    if not url:
        return ""
    return url.split("?")[0].rstrip("/")


async def _process_manual_projects(
    project_list: list[dict], service: ProjectService | ApplicationService, default_source: str, model_class=Project
):
    """
    Helper to process manual project/application entries.
    """
    existing_items = await service.list()
    existing_urls = {normalize_url(p.repo_url): p.id for p in existing_items if p.repo_url}
    existing_demo_urls = {normalize_url(p.demo_url): p.id for p in existing_items if p.demo_url}

    for proj_data in project_list:
        # Enforce manual flags if not already set
        proj_data.setdefault("is_manual", True)
        proj_data.setdefault("source_platform", default_source)

        try:
            p = model_class(**proj_data)
        except Exception as validation_err:
            console.print(f"[red]Validation Error for {default_source} {proj_data.get('title')}: {validation_err}[/red]")
            continue

        # Map for titles
        existing_title_map = {}
        ambiguous_titles = set()
        for existing_p in existing_items:
            if existing_p.title in existing_title_map:
                ambiguous_titles.add(existing_p.title)
            existing_title_map[existing_p.title] = existing_p.id

        match_id = None
        norm_repo = normalize_url(p.repo_url)
        norm_demo = normalize_url(p.demo_url)

        if norm_repo and norm_repo in existing_urls:
            match_id = existing_urls[norm_repo]
        elif norm_demo and norm_demo in existing_demo_urls:
            match_id = existing_demo_urls[norm_demo]
        elif p.title in existing_title_map:
            if p.title in ambiguous_titles:
                console.print(
                    f"[bold red]Error: Title '{p.title}' matches multiple existing items. Cannot safely upsert by title. Skipping.[/bold red]"
                )
                continue
            match_id = existing_title_map[p.title]

        desired_id = None
        if p.id:
            desired_id = p.id
        elif p.repo_url:
            desired_id = f"{default_source}:{slugify(p.repo_url.rstrip('/').split('/')[-1])}"
        elif p.demo_url:
            desired_id = f"{default_source}:{slugify(p.demo_url.rstrip('/').split('/')[-1])}"
        else:
            desired_id = f"{default_source}:{slugify(p.title)}"

        if match_id:
            p.id = match_id
            await service.update(p.id, p.model_dump(exclude={"id"}))
            console.print(f"Updated {default_source.capitalize()}: {p.title}")
        else:
            await service.create(p, item_id=desired_id)
            console.print(f"Created {default_source.capitalize()}: {p.title} (ID: {desired_id})")


async def _migrate_existing_items(blog_service, project_service, application_service):
    """
    Renames existing documents to use the platform-prefixed slug ID format.
    Also handles basic deduplication by URL.
    """
    console.print("[bold blue]Checking for ID migration and deduplication...[/bold blue]")

    async def process_collection(service, prefix_extractor):
        items = await service.list()
        url_map = {}
        for item in items:
            url = None
            if hasattr(item, "url") and item.url:
                url = normalize_url(item.url)
            elif hasattr(item, "repo_url") and item.repo_url:
                url = normalize_url(item.repo_url)
            elif hasattr(item, "demo_url") and item.demo_url:
                url = normalize_url(item.demo_url)

            if not url:
                continue

            if url not in url_map:
                url_map[url] = []
            url_map[url].append(item)

        seen_expected_ids = set()
        for url, group in url_map.items():
            first_item = group[0]
            prefix = prefix_extractor(first_item)
            title_slug = slugify(first_item.title)
            if not title_slug:
                title_slug = slugify(url.split("/")[-1]) or "untitled"

            expected_id = f"{prefix}:{title_slug}"

            # Basic collision avoidance for different URLs with same title
            if expected_id in seen_expected_ids:
                expected_id = f"{expected_id}-{slugify(url[-10:])}"
            seen_expected_ids.add(expected_id)

            # Pick the best item from duplicates
            best_item = first_item
            if len(group) > 1:
                best_item = max(
                    group,
                    key=lambda x: (
                        1 if getattr(x, "ai_summary", None) else 0,
                        1 if getattr(x, "markdown_content", None) else 0,
                        len(getattr(x, "tags", [])),
                    ),
                )
                console.print(f"[yellow]Merging {len(group)} duplicates for {url}[/yellow]")

            # Migrate or clean up duplicates
            if best_item.id != expected_id or len(group) > 1:
                # CRITICAL FIX: Clear the ID on the model so service.create uses our expected_id
                migrated_item = best_item.model_copy(update={"id": None})
                await service.create(migrated_item, item_id=expected_id)

                # Delete all others in the group (including the old version if ID changed)
                for item in group:
                    if item.id != expected_id:
                        await service.delete(item.id)
                        console.print(f"[dim]Removed old/duplicate ID: {item.id}[/dim]")

                if best_item.id != expected_id:
                    console.print(f"Migrated: {best_item.id} -> {expected_id}")

    try:
        await process_collection(blog_service, lambda b: (b.platform or "medium").lower().replace(".", ""))
        await process_collection(project_service, lambda p: (p.source_platform or "github").lower())
        await process_collection(application_service, lambda a: "application")
    except Exception as e:
        console.print(f"[bold red]Warning: ID migration pass failed:[/bold red] {e}")


async def ingest_resources(
    github_user: str | None,
    medium_user: str | None,
    medium_zip: str | None,
    devto_user: str | None,
    yaml_file: str | None,
    about_file: str | None,
    project_id: str,
):
    """Ingests portfolio resources from various sources into Firestore."""

    db = firestore.AsyncClient(project=project_id)
    project_service = ProjectService(db)
    application_service = ApplicationService(db)
    blog_service = BlogService(db)
    content_service = ContentService(db)

    # 0. Migrate existing data to new ID format
    await _migrate_existing_items(blog_service, project_service, application_service)

    # Statistics tracking
    stats = {
        "github": {"new": 0, "updated": 0, "skipped": 0},
        "medium": {"new": 0, "updated": 0, "skipped": 0, "drafts": 0, "filtered": 0},
        "devto": {"new": 0, "updated": 0, "skipped": 0, "filtered": 0, "enriched": 0},
        "manual": {"new": 0, "updated": 0, "skipped": 0},
        "about": {"updated": 0},
    }

    # --- About Page ---
    if about_file:
        console.print(f"[bold blue]Processing About File: {about_file}...[/bold blue]")
        try:
            with open(about_file, encoding="utf-8") as f:
                about_body = f.read()

            content = Content(title="About", body=about_body, last_updated=datetime.now(UTC))
            # Create or update 'about' document
            await content_service.create(content, item_id="about")
            console.print("[green]Successfully updated About page content.[/green]")
            stats["about"]["updated"] += 1
        except Exception as e:
            console.print(f"[bold red]Error processing About file:[/bold red] {e}")

    # --- GitHub ---
    if github_user:
        console.print(f"[bold blue]Fetching GitHub repos for {github_user}...[/bold blue]")
        connector = GitHubConnector()
        try:
            projects = await connector.fetch_repositories(github_user)
            console.print(f"Found {len(projects)} repositories.")

            existing_projects = await project_service.list()
            existing_urls = {normalize_url(p.repo_url): p.id for p in existing_projects if p.repo_url}

            for p in projects:
                normalized_url = normalize_url(p.repo_url)
                if normalized_url in existing_urls:
                    p.id = existing_urls[normalized_url]
                    await project_service.update(p.id, p.model_dump(exclude={"id"}))
                    console.print(f"Updated: {p.title}")
                    stats["github"]["updated"] += 1
                else:
                    slug = f"github:{slugify(p.title)}"
                    await project_service.create(p, item_id=slug)
                    console.print(f"Created: {p.title} (ID: {slug})")
                    stats["github"]["new"] += 1

        except Exception as e:
            console.print(f"[bold red]Error fetching GitHub:[/bold red] {e}")

    # --- Medium (Hybrid) ---
    if medium_user or medium_zip:
        console.print("[bold blue]Processing Medium content...[/bold blue]")

        # 1. Fetch RSS feeds first (if enabled)
        rss_posts: list[Blog] = []
        if medium_user:
            console.print(f"Fetching RSS feed for {medium_user}...")
            rss_connector = MediumConnector()
            try:
                rss_posts = await rss_connector.fetch_posts(medium_user)
                console.print(f"Found {len(rss_posts)} Medium posts in RSS.")
            except Exception as e:
                console.print(f"[bold red]Error fetching Medium RSS:[/bold red] {e}")

        # 2. Pre-fetch existing Firestore blogs for efficient upsert
        console.print("Fetching existing Firestore blogs...")
        existing_blogs = await blog_service.list()
        existing_blog_map = {normalize_url(b.url): b for b in existing_blogs if b.url}

        # 3. Process Archive (streaming)
        if medium_zip:
            console.print("[bold blue]Processing Medium archive...[/bold blue]")
            enrichment_service = ContentEnrichmentService()
            archive_connector = MediumArchiveConnector(ai_service=enrichment_service)
            try:
                # Count total files first
                total_files_in_zip = 0
                try:
                    with zipfile.ZipFile(medium_zip, "r") as z:
                        total_files_in_zip = len([f for f in z.namelist() if f.startswith("posts/") and f.endswith(".html")])
                        if total_files_in_zip > 0:
                            console.print(f"Found {total_files_in_zip} blog posts to process.")
                        else:
                            console.print("[yellow]No blog posts found in the archive.[/yellow]")
                except FileNotFoundError:
                    console.print(f"[bold red]Error: Zip file not found at {medium_zip}[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]Error reading zip file metadata:[/bold red] {e}")

                if total_files_in_zip > 0:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(bar_width=None),
                        TaskProgressColumn(),
                        TimeRemainingColumn(),
                        console=console,
                        redirect_stdout=False,
                        redirect_stderr=False,
                    ) as progress:
                        task_id = progress.add_task("Processing Medium Archive...", total=total_files_in_zip)

                        def update_progress(processed, total, current_file, phase):
                            short_file = os.path.basename(current_file)
                            if len(short_file) > 30:
                                short_file = short_file[:27] + "..."
                            progress.update(
                                task_id,
                                completed=processed,
                                total=total,
                                description=f"[cyan]{phase:18}[/cyan] [white]{short_file}[/white]",
                            )

                        # Stream results from generator
                        # We pass map of URLs that already have ai_summary to skip them
                        urls_to_skip = {url for url, b in existing_blog_map.items() if b.ai_summary}
                        async for status, blog, filename in archive_connector.fetch_posts(
                            medium_zip, existing_urls=urls_to_skip, on_progress=update_progress
                        ):
                            if status == "skipped_draft":
                                stats["medium"]["drafts"] += 1
                                console.log(f"[yellow]Skipping (draft):[/yellow] {os.path.basename(filename)}")
                                continue

                            if status == "skipped_not_blog":
                                stats["medium"]["filtered"] += 1
                                console.log(f"[yellow]Skipping (not a blog):[/yellow] {os.path.basename(filename)}")
                                continue

                            if status == "skipped_existing":
                                stats["medium"]["skipped"] += 1
                                continue

                            if status == "error":
                                console.log(f"[red]Error processing:[/red] {os.path.basename(filename)}")
                                continue

                            if status == "processed" and blog:
                                # Merge with RSS if available
                                matched_rss = next((p for p in rss_posts if normalize_url(p.url) == normalize_url(blog.url)), None)
                                if matched_rss:
                                    blog.title = matched_rss.title
                                    blog.date = matched_rss.date
                                    rss_posts.remove(matched_rss)

                                # Persist immediately
                                normalized_url = normalize_url(blog.url)
                                if normalized_url in existing_blog_map:
                                    blog.id = existing_blog_map[normalized_url].id
                                    await blog_service.update(blog.id, blog.model_dump(exclude={"id"}))
                                    stats["medium"]["updated"] += 1
                                else:
                                    slug = f"medium:{slugify(blog.title)}"
                                    await blog_service.create(blog, item_id=slug)
                                    stats["medium"]["new"] += 1

            except Exception as e:
                console.print(f"[bold red]Error parsing Medium archive:[/bold red] {e}")

        # 4. Process remaining RSS blogs (those not in archive)
        if rss_posts:
            enrichment_service = ContentEnrichmentService()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing Medium RSS...", total=len(rss_posts))

                for blog in rss_posts:
                    progress.update(task, description=f"[cyan]Processing[/cyan] [white]{blog.title[:30]}...[/white]")
                    normalized_url = normalize_url(blog.url)
                    existing = existing_blog_map.get(normalized_url)

                    # 1. Skip if already exists and has summary
                    if existing and existing.ai_summary:
                        stats["medium"]["skipped"] += 1
                        progress.advance(task)
                        continue

                    # 2. Enrich if we have content and summary is missing
                    if blog.markdown_content and (not existing or not existing.ai_summary):
                        progress.update(task, description=f"[green]Enriching[/green] [white]{blog.title[:30]}...[/white]")
                        try:
                            enrichment = await enrichment_service.enrich_content(blog.markdown_content)
                            blog.ai_summary = enrichment.get("summary")
                            ai_tags = enrichment.get("tags")
                            if ai_tags:
                                blog.tags = ai_tags
                            stats["medium"]["enriched"] = stats["medium"].get("enriched", 0) + 1
                        except Exception as e:
                            console.log(f"[red]Enrichment failed for {blog.title}:[/red] {e}")

                    # 3. Persist
                    progress.update(task, description=f"[blue]Saving[/blue] [white]{blog.title[:30]}...[/white]")
                    if existing:
                        blog.id = existing.id
                        await blog_service.update(blog.id, blog.model_dump(exclude={"id"}))
                        stats["medium"]["updated"] += 1
                    else:
                        slug = f"medium:{slugify(blog.title)}"
                        await blog_service.create(blog, item_id=slug)
                        stats["medium"]["new"] += 1

                    progress.advance(task)

    # --- Dev.to ---
    if devto_user:
        console.print(f"[bold blue]Fetching Dev.to posts for {devto_user}...[/bold blue]")
        connector = DevToConnector()
        try:
            # Pre-fetch existing Firestore blogs for efficient upsert
            existing_blogs = await blog_service.list()
            existing_blog_map = {normalize_url(b.url): b for b in existing_blogs if b.url}
            urls_to_skip_detail = {url for url, b in existing_blog_map.items() if b.ai_summary}

            # We fetch all basic metadata first
            blogs = await connector.fetch_posts(devto_user, existing_urls=urls_to_skip_detail)
            console.print(f"Found {len(blogs)} Dev.to posts (filtered).")

            enrichment_service = ContentEnrichmentService()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Processing Dev.to posts...", total=len(blogs))

                for b in blogs:
                    progress.update(task, description=f"[cyan]Processing[/cyan] [white]{b.title[:30]}...[/white]")

                    normalized_url = normalize_url(b.url)
                    existing = existing_blog_map.get(normalized_url)

                    # 1. Skip if already exists and has summary
                    if existing and existing.ai_summary:
                        stats["devto"]["skipped"] += 1
                        progress.advance(task)
                        continue

                    # 2. Enrich if missing summary
                    if b.markdown_content:
                        progress.update(task, description=f"[green]Enriching[/green] [white]{b.title[:30]}...[/white]")
                        try:
                            enrichment = await enrichment_service.enrich_content(b.markdown_content)
                            b.ai_summary = enrichment.get("summary")
                            ai_tags = enrichment.get("tags")
                            if ai_tags:
                                b.tags = ai_tags
                            stats["devto"]["enriched"] += 1
                        except Exception as e:
                            console.log(f"[red]Enrichment failed for {b.title}:[/red] {e}")

                    # 3. Persist
                    progress.update(task, description=f"[blue]Saving[/blue] [white]{b.title[:30]}...[/white]")
                    if existing:
                        b.id = existing.id
                        await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                        stats["devto"]["updated"] += 1
                    else:
                        slug = f"devto:{slugify(b.title)}"
                        await blog_service.create(b, item_id=slug)
                        stats["devto"]["new"] += 1

                    progress.advance(task)

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
                await _process_manual_projects(manual_projects, project_service, "manual")

            # Process Applications
            manual_apps = data.get("applications", [])
            if manual_apps:
                console.print(f"Found {len(manual_apps)} manual applications.")
                valid_apps = []
                # For applications, we enforce some defaults and validation
                for app_data in manual_apps:
                    app_data["featured"] = True
                    app_data["source_platform"] = "application"
                    if not app_data.get("demo_url"):
                        console.print(
                            f"[bold red]Error: Application '{app_data.get('title')}' is missing the required 'demo_url'. Skipping.[/bold red]"
                        )
                        continue
                    valid_apps.append(app_data)

                if valid_apps:
                    await _process_manual_projects(valid_apps, application_service, "application", model_class=Application)

            # Process Blogs
            manual_blogs = data.get("blogs", [])
            if manual_blogs:
                console.print(f"Found {len(manual_blogs)} manual blogs.")
                existing_blogs = await blog_service.list()
                existing_blog_map = {normalize_url(b.url): b for b in existing_blogs if b.url}

                for blog_data in manual_blogs:
                    blog_data["is_manual"] = True
                    blog_data["source_platform"] = "manual"

                    try:
                        b = Blog(**blog_data)
                    except Exception as validation_err:
                        console.print(f"[red]Validation Error for blog {blog_data.get('title')}: {validation_err}[/red]")
                        continue

                    existing = existing_blog_map.get(normalize_url(b.url))
                    desired_id = None
                    if b.id:
                        desired_id = b.id
                    elif b.url:
                        # try to get slug from url
                        desired_id = f"manual:{slugify(normalize_url(b.url).split('/')[-1])}"
                    else:
                        console.print(
                            f"[yellow]Warning: No 'id' or 'url' for manual blog '{b.title}'. Using title slug as ID. This may not be stable.[/yellow]"
                        )
                        desired_id = f"manual:{slugify(b.title)}"

                    if existing:
                        b.id = existing.id
                        await blog_service.update(b.id, b.model_dump(exclude={"id"}))
                        console.print(f"Updated Manual: {b.title}")
                        stats["manual"]["updated"] += 1
                    else:
                        await blog_service.create(b, item_id=desired_id)
                        console.print(f"Created Manual: {b.title} (ID: {desired_id})")
                        stats["manual"]["new"] += 1

        except Exception as e:
            console.print(f"[bold red]Error processing YAML:[/bold red] {e}")

    # --- FINAL SUMMARY ---
    console.print("\n" + "=" * 50)
    console.print("[bold green]Ingestion Summary[/bold green]")
    console.print("=" * 50)

    for platform, data in stats.items():
        if sum(data.values()) > 0:
            console.print(f"[bold cyan]{platform.upper()}[/bold cyan]")
            summary_parts = []
            if data.get("new"): summary_parts.append(f"New: {data['new']}")
            if data.get("updated"): summary_parts.append(f"Updated/Patched: {data['updated']}")
            if data.get("enriched"): summary_parts.append(f"AI Enriched: {data['enriched']}")
            if data.get("skipped"): summary_parts.append(f"Skipped (existing): {data['skipped']}")
            if data.get("filtered"): summary_parts.append(f"Filtered (quickies): {data['filtered']}")
            if data.get("drafts"): summary_parts.append(f"Drafts: {data['drafts']}")
            console.print("  " + ", ".join(summary_parts))

    console.print("=" * 50)


@app.command()
def main(
    github_user: str = typer.Option(None, help="GitHub username"),
    medium_user: str = typer.Option(None, help="Medium username"),
    medium_zip: str = typer.Option(None, help="Path to Medium export zip file"),
    devto_user: str = typer.Option(None, help="Dev.to username"),
    yaml_file: str = typer.Option(None, help="Path to manual resources YAML file"),
    about_file: str = typer.Option(None, help="Path to Markdown file for About page"),
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

    asyncio.run(ingest_resources(github_user, medium_user, medium_zip, devto_user, yaml_file, about_file, project_id))


if __name__ == "__main__":
    app()
