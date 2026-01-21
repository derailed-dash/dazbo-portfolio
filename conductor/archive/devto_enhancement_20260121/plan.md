# Implementation Plan: Enhance Dev.to Ingestion

This plan outlines the steps to filter out "Quickie" posts, enable AI enrichment, and capture Markdown content for Dev.to blog posts during ingestion.

## Phase 1: Filtering and Model Alignment [checkpoint: 3248550]
Goal: Implement the "Boost" filter and ensure the Dev.to connector captures the required content fields.

- [x] Task: Write unit tests for `DevToConnector.fetch_posts` filtering logic c73b950
    - [x] Test that titles starting with `[Boost]` are excluded
    - [x] Test that regular titles are included
- [x] Task: Implement title filtering in `DevToConnector.fetch_posts` c73b950
- [x] Task: Update `DevToConnector` to fetch full article content (Markdown) 4c1465e
    - [x] Update API call to retrieve `body_markdown`
    - [x] Map `body_markdown` to `Blog.markdown_content`
- [x] Task: Verify filtering and content retrieval with tests 4c1465e
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: AI Enrichment Integration [checkpoint: 4a9d6aa]
Goal: Integrate `ContentEnrichmentService` to provide technical summaries and tags for Dev.to posts.

- [x] Task: Write unit tests for AI enrichment integration in `DevToConnector` da91440
    - [x] Mock `ContentEnrichmentService` to return predictable summaries/tags
    - [x] Verify `ai_summary` and `tags` are populated in the returned `Blog` objects
- [x] Task: Implement AI enrichment in `DevToConnector.fetch_posts` da91440
    - [x] Call `ContentEnrichmentService.enrich_content` (passing Markdown content)
    - [x] Ensure summary limit is set to 225 words in the prompt context
    - [x] Implement error handling/fallback to original metadata
- [x] Task: Verify enrichment logic with tests da91440
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: CLI Integration and E2E Verification [checkpoint: 5570f4e]
Goal: Ensure the ingestion tool provides correct feedback and performs E2E updates to Firestore.

- [x] Task: Update `app/tools/ingest.py` to support Dev.to enrichment feedback d9b2659
    - [x] Ensure logging shows "Enriching content..." for Dev.to posts
    - [x] Ensure logging shows "Skipping (quickie)" for filtered posts
    - [x] Implement visual progress indicator (spinner or bar) for Dev.to ingestion
- [x] Task: Write/Update integration test for Dev.to ingestion b0a35ac
    - [x] Mock Dev.to API and AI service
    - [x] Verify the full flow from API to `Blog` model population
- [x] Task: Run full ingestion for a test Dev.to user and verify Firestore results
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
