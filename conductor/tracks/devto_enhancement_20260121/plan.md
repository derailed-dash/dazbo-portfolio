# Implementation Plan: Enhance Dev.to Ingestion

This plan outlines the steps to filter out "Quickie" posts, enable AI enrichment, and capture Markdown content for Dev.to blog posts during ingestion.

## Phase 1: Filtering and Model Alignment
Goal: Implement the "Boost" filter and ensure the Dev.to connector captures the required content fields.

- [x] Task: Write unit tests for `DevToConnector.fetch_posts` filtering logic c73b950
    - [x] Test that titles starting with `[Boost]` are excluded
    - [x] Test that regular titles are included
- [x] Task: Implement title filtering in `DevToConnector.fetch_posts` c73b950
- [x] Task: Update `DevToConnector` to fetch full article content (Markdown) 4c1465e
    - [x] Update API call to retrieve `body_markdown`
    - [x] Map `body_markdown` to `Blog.markdown_content`
- [x] Task: Verify filtering and content retrieval with tests 4c1465e
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: AI Enrichment Integration
Goal: Integrate `ContentEnrichmentService` to provide technical summaries and tags for Dev.to posts.

- [ ] Task: Write unit tests for AI enrichment integration in `DevToConnector`
    - [ ] Mock `ContentEnrichmentService` to return predictable summaries/tags
    - [ ] Verify `ai_summary` and `tags` are populated in the returned `Blog` objects
- [ ] Task: Implement AI enrichment in `DevToConnector.fetch_posts`
    - [ ] Call `ContentEnrichmentService.enrich_content` (passing Markdown content)
    - [ ] Ensure summary limit is set to 225 words in the prompt context
    - [ ] Implement error handling/fallback to original metadata
- [ ] Task: Verify enrichment logic with tests
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: CLI Integration and E2E Verification
Goal: Ensure the ingestion tool provides correct feedback and performs E2E updates to Firestore.

- [ ] Task: Update `app/tools/ingest.py` to support Dev.to enrichment feedback
    - [ ] Ensure logging shows "Enriching content..." for Dev.to posts
    - [ ] Ensure logging shows "Skipping (quickie)" for filtered posts
- [ ] Task: Write/Update integration test for Dev.to ingestion
    - [ ] Mock Dev.to API and AI service
    - [ ] Verify the full flow from API to `Blog` model population
- [ ] Task: Run full ingestion for a test Dev.to user and verify Firestore results
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
