# Implementation Plan: Comprehensive Medium Blog Ingestion

## Phase 1: Model Updates and AI Tooling
- [ ] Task: Update `Blog` model
    - [ ] Task: Add `is_private` (bool), `markdown_content` (str), `ai_summary` (str) fields to `app/models/blog.py`.
- [ ] Task: Create AI Summarization Service
    - [ ] Task: Implement a helper function/service that accepts text and returns a Gemini-generated summary.
    - [ ] Task: Create tests for this service (mocking the LLM response).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Model Updates and AI Tooling' (Protocol in workflow.md)

## Phase 2: Medium Archive Parser & Markdown Converter
- [ ] Task: Create tests for `MediumArchiveConnector` and Markdown conversion
    - [ ] Task: Test HTML -> Markdown conversion logic (H1, H2, H3 rules).
    - [ ] Task: Test Frontmatter extraction.
    - [ ] Task: Test paywall heuristic detection.
- [ ] Task: Implement `MediumArchiveConnector` with Conversion Logic
    - [ ] Task: Implement `app/services/connectors/medium_archive_connector.py`.
    - [ ] Task: Use a library like `markdownify` or `BeautifulSoup` to handle the conversion.
    - [ ] Task: Integrate the AI Summarization Service to generate summaries for each post.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Medium Archive Parser & Markdown Converter' (Protocol in workflow.md)

## Phase 3: CLI Integration and Hybrid Logic
- [ ] Task: Update Ingestion Logic (`app/tools/ingest.py`)
    - [ ] Task: Add `--medium-zip` argument.
    - [ ] Task: Implement the priority logic: Use RSS for latest metadata, but enrich *all* matching posts (RSS or Zip) with the Markdown content from the Zip if available.
    - [ ] Task: **Explicitly persist updates to Firestore:** Ensure `BlogService.update` is called to save `markdown_content`, `ai_summary`, and `is_private` for existing and new records.
- [ ] Task: Integration Tests
    - [ ] Task: Verify that a post existing in both RSS and Zip gets the correct merged data (fresh date from RSS, full content from Zip).
    - [ ] Task: Verify that Firestore documents are correctly updated with the new fields.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: CLI Integration and Hybrid Logic' (Protocol in workflow.md)

## Phase 4: UI Updates
- [ ] Task: Update Frontend Blog Display
    - [ ] Task: Update the Blog Card component to display the `ai_summary`.
    - [ ] Task: Ensure the "Read More" link points to the original Medium URL.
    - [ ] Task: Display the "Member-only" badge.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: UI Updates' (Protocol in workflow.md)
