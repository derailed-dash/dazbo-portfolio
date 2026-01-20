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

## Phase 3: CLI Integration and Hybrid Logic [checkpoint: b4582da]
- [x] Task: Update Ingestion Logic (`app/tools/ingest.py`)
    - [x] Task: Add `--medium-zip` argument.
    - [x] Task: Implement the priority logic: Use RSS for latest metadata, but enrich *all* matching posts (RSS or Zip) with the Markdown content from the Zip if available.
    - [x] Task: **Explicitly persist updates to Firestore:** Ensure `BlogService.update` is called to save `markdown_content`, `ai_summary`, and `is_private` for existing and new records.
- [x] Task: Add rich progress reporting to `MediumArchiveConnector` and `ingest.py`.
- [x] Task: Integration Tests
    - [x] Task: Verify that a post existing in both RSS and Zip gets the correct merged data (fresh date from RSS, full content from Zip).
    - [x] Task: Verify that Firestore documents are correctly updated with the new fields.
- [x] Task: Conductor - User Manual Verification 'Phase 3: CLI Integration and Hybrid Logic' (Protocol in workflow.md)

## Phase 4: UI Updates and Documentation [checkpoint: 9f2f702]
- [x] Task: Update Frontend Blog Display
    - [x] Task: Update the Blog Card component to display the `ai_summary`.
    - [x] Task: Ensure the "Read More" link points to the original Medium URL.
    - [x] Task: Display the "Member-only" badge.
- [x] Task: Update Documentation
    - [x] Task: Update `docs/design-and-walkthrough.md` with:
        - [x] New design decision (Hybrid Ingestion, AI Summarization).
        - [x] Detailed walkthrough of the `MediumArchiveConnector` and the ingestion pipeline.
        - [x] Explanation of how we establish when we should insert / upsert / skip (and why).
        - [x] How we're providing UI feedback in the console.
- [x] Task: Conductor - User Manual Verification 'Phase 4: UI Updates and Documentation' (Protocol in workflow.md)