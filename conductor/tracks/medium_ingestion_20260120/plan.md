# Implementation Plan: Comprehensive Medium Blog Ingestion

## Phase 1: Model Updates and AI Tooling [checkpoint: 8861ec7]
- [x] Task: Update `Blog` model
    - [x] Task: Add `is_private` (bool), `markdown_content` (str), `ai_summary` (str) fields to `app/models/blog.py`.
- [x] Task: Create AI Summarization Service
    - [x] Task: Implement a helper function/service that accepts text and returns a Gemini-generated summary.
    - [x] Task: Create tests for this service (mocking the LLM response).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Model Updates and AI Tooling' (Protocol in workflow.md)

## Phase 2: Medium Archive Parser & Markdown Converter [checkpoint: b314cc7]
- [x] Task: Create tests for `MediumArchiveConnector` and Markdown conversion
    - [x] Task: Test HTML -> Markdown conversion logic (H1, H2, H3 rules).
    - [x] Task: Test Frontmatter extraction.
    - [x] Task: Test paywall heuristic detection.
- [x] Task: Implement `MediumArchiveConnector` with Conversion Logic
    - [x] Task: Implement `app/services/connectors/medium_archive_connector.py`.
    - [x] Task: Use a library like `markdownify` or `BeautifulSoup` to handle the conversion.
    - [x] Task: Integrate the AI Summarization Service to generate summaries for each post.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Medium Archive Parser & Markdown Converter' (Protocol in workflow.md)

## Phase 3: CLI Integration and Hybrid Logic
- [ ] Task: Update Ingestion Logic (`app/tools/ingest.py`)
    - [ ] Task: Add `--medium-zip` argument.
    - [ ] Task: Implement the priority logic: Use RSS for latest metadata, but enrich *all* matching posts (RSS or Zip) with the Markdown content from the Zip if available.
    - [ ] Task: **Explicitly persist updates to Firestore:** Ensure `BlogService.update` is called to save `markdown_content`, `ai_summary`, and `is_private` for existing and new records.
- [ ] Task: Integration Tests
    - [ ] Task: Verify that a post existing in both RSS and Zip gets the correct merged data (fresh date from RSS, full content from Zip).
    - [ ] Task: Verify that Firestore documents are correctly updated with the new fields.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: CLI Integration and Hybrid Logic' (Protocol in workflow.md)

## Phase 4: UI Updates and Documentation
- [ ] Task: Update Frontend Blog Display
    - [ ] Task: Update the Blog Card component to display the `ai_summary`.
    - [ ] Task: Ensure the "Read More" link points to the original Medium URL.
    - [ ] Task: Display the "Member-only" badge.
- [ ] Task: Update Documentation
    - [ ] Task: Update `docs/design-and-walkthrough.md` with:
        - [ ] New design decision (Hybrid Ingestion, AI Summarization).
        - [ ] Detailed walkthrough of the `MediumArchiveConnector` and the ingestion pipeline.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: UI Updates and Documentation' (Protocol in workflow.md)