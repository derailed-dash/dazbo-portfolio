# Specification: Portfolio Resource Ingestion Strategy

## Overview
This track defines and implements the system for bringing portfolio resources—including blog posts, GitHub repositories, websites, and applications—into the Dazbo Portfolio application. It focuses on a decoupled, "out-of-band" ingestion process via CLI scripts that populate Google Firestore and handle static assets via Google Cloud Storage.

## Goals
- Establish a "Source of Truth" in Firestore for all showcaseable items.
- Provide a hybrid ingestion mechanism (automated connectors + manual entries).
- Enable on-demand triggering via a dedicated CLI tool.
- Support metadata-only entries for paywalled or external content.

## Functional Requirements

### 1. Ingestion Connectors
- **GitHub Connector:** Fetch public repositories, metadata (stars, description), and primary languages.
- **Medium Connector:** Fetch blog post metadata (titles, links, summaries).
- **Dev.to Connector:** Fetch blog post metadata via the Dev.to API.
- **Custom/Manual Connector:** Support for entries not tied to a specific platform (e.g., private projects, paywalled articles, standalone websites).

### 2. Ingestion Triggering
- **CLI Tooling:** A set of Python scripts in `scripts/` or a dedicated module (e.g., `app/tools/ingest.py`) to trigger syncs manually from a developer environment.

### 3. Static Asset Management
- **Image Storage:** All portfolio-related images (thumbnails, profile pics, screenshots) will be stored in a **Public Google Cloud Storage (GCS) Bucket**.
- **Asset Referencing:** Firestore documents will store the public URLs of these GCS objects.

### 4. Data Architecture
- **Decoupled Logic:** The ingestion logic will be kept separate from the main FastAPI request-response cycle to minimize dependencies in the production runtime.
- **Schema Support:** Extend/Verify `Project` and `Blog` models to support "manual" flags and "metadata-only" status.

## Non-Functional Requirements
- **Resilience:** Handle API rate limiting and transient network errors gracefully.
- **Maintainability:** Use a modular "Connector" pattern to allow adding new sources easily.
- **Idempotency:** Ensure that repeated ingestion runs do not create duplicate entries in Firestore.

## Acceptance Criteria
- [ ] A Python script exists that can sync GitHub, Medium, and Dev.to content to Firestore.
- [ ] Ability to manually add a "Custom" resource entry via a configuration file (e.g., YAML) processed by the CLI.
- [ ] Images successfully uploaded to GCS are accessible via public URL in the app.
- [ ] Integration tests verify that ingestion does not create duplicate entries.

## Out of Scope
- A full-blown web-based Admin Dashboard (GUI).
- Admin API endpoints.
- Automated crawling of paywalled content body (metadata/stubs only).
- Real-time Webhook-based syncing.
- LinkedIn Connector.
