# Specification: Application and Project Separation

## Overview
This track aims to cleanly separate "Applications" from "Featured Projects" in the portfolio. "Featured Projects" will be dedicated to public GitHub repositories (excluding forks), while "Applications" (renamed from "Live Applications") will showcase manually curated applications ingested via YAML.

## Functional Requirements
- **Ingestion (GitHub):**
    - Update `GitHubConnector` to identify and skip repositories that are forks.
    - Ensure only original public repositories are ingested as "Projects".
- **Ingestion (Manual YAML):**
    - Update `app/tools/ingest.py` to support an `applications:` heading in the YAML file.
    - Entries under `applications:` must automatically be assigned `featured=true`, `is_manual=true`, and `source_platform="application"`.
    - For `applications:`, `demo_url` is mandatory, but `repo_url` is optional.
- **Frontend (UI/UX):**
    - Rename the "Live Applications" section to "Applications" in `AppsCarousel.tsx`.
    - Update `ProjectCarousel.tsx` to only display projects where `source_platform === "github"`.
    - Update `AppsCarousel.tsx` to only display projects where `source_platform === "application"`.
    - Remove hardcoded mock data from `AppsCarousel.tsx`.
- **Documentation:**
    - Update `docs/design-and-walkthrough.md` to reflect the new YAML schema and the separation logic.

## Non-Functional Requirements
- **Consistency:** Maintain consistent card styling across both carousels.
- **Performance:** Ensure filtering happens efficiently on the client-side (or via API if preferred, but client-side is current pattern).

## Acceptance Criteria
- [ ] `uv run python -m app.tools.ingest --github-user ...` does not ingest any forks.
- [ ] `uv run python -m app.tools.ingest --yaml-file ...` correctly processes the `applications:` section.
- [ ] The "Featured Projects" carousel only shows GitHub repositories.
- [ ] The "Applications" carousel only shows items from the manual YAML `applications:` section.
- [ ] Images from GCS (provided as URLs) render correctly in both carousels.
- [ ] Documentation accurately describes the `applications:` YAML heading.

## Out of Scope
- Automated GCS image uploading (images must still be manually uploaded to GCS and their URLs provided in YAML).
- Multi-user support for ingestion.
