# Track Specification - Ingestion Tool Refinement

## Overview
This track focuses on optimizing the content ingestion tool (`app/tools/ingest.py`) to prevent redundant processing, improve data quality from Medium and dev.to, and ensure project documentation remains thorough and accurate.

## Functional Requirements
- **Idempotency Logic**: 
    - Use a slug-based ID derived from the article title.
    - Scope the unique ID to the source platform (e.g., `medium:my-article-title` and `devto:my-article-title` are distinct).
    - Skip ingestion if the document already exists in Firestore AND contains a valid `ai_summary`.
- **Mandatory Metadata Patching**: 
    - If a document exists but is missing the `ai_summary` field, the tool must proceed with ingestion/AI enrichment to "patch" the record.
- **dev.to "Quickie" Filtering**: 
    - Automatically ignore dev.to articles where the body content is less than 200 words.
- **Cross-Platform Support**: 
    - Ensure cross-posted articles (same title on different platforms) are treated as unique entities in the database.

## Documentation & Testing
- **Design Update**: Update `docs/design-and-walkthrough.md` to accurately describe the platform-scoped idempotency logic and the filtering criteria.
- **Testing Update**: Update `docs/testing.md` to document any new unit or integration tests added during this track.

## Acceptance Criteria
- [ ] Ingestion tool identifies existing posts using platform-scoped slug IDs.
- [ ] Ingestion tool skips processing for posts that already have an `ai_summary`.
- [ ] Ingestion tool successfully updates/patches existing posts if `ai_summary` is missing.
- [ ] dev.to articles with < 200 words are filtered out and logged as skipped.
- [ ] Identical titles from different platforms result in separate Firestore documents.
- [ ] `docs/design-and-walkthrough.md` is updated and thorough regarding ingestion.
- [ ] `docs/testing.md` is updated with details of new tests.

## Out of Scope
- Automatic deletion of removed articles from source platforms.
- Retroactive filtering of existing articles in Firestore that are under 200 words.
