# Implementation Plan - Ingestion Tool Refinement

This plan outlines the steps to optimize the content ingestion tool to prevent redundant processing, improve data quality, and update project documentation.

## Phase 1: Idempotency & Metadata Patching
This phase focuses on implementing the platform-scoped unique identification and the intelligent skip logic based on mandatory metadata.

- [ ] Task: Create unit tests for platform-scoped idempotency and metadata patching
    - [ ] Add test cases to `tests/unit/test_ingest_cli.py` or a new test file for platform-scoped IDs.
    - [ ] Add test cases for the "skip if exists and has ai_summary" logic.
    - [ ] Verify that tests fail as expected (Red Phase).
- [ ] Task: Implement platform-scoped slug ID and ai_summary presence check in `app/tools/ingest.py`
    - [ ] Update the ID generation logic to include a platform prefix.
    - [ ] Modify the `skipped_existing` check to also verify the presence of the `ai_summary` field.
    - [ ] Ensure that existing records missing `ai_summary` are processed for enrichment.
    - [ ] Verify that all unit tests pass (Green Phase).
- [ ] Task: Conductor - User Manual Verification 'Idempotency & Metadata Patching' (Protocol in workflow.md)

## Phase 2: dev.to "Quickie" Filtering
This phase focuses on filtering out short, non-article content from dev.to.

- [ ] Task: Create unit tests for dev.to word count filtering
    - [ ] Add test cases to `tests/unit/test_devto_connector.py` for filtering articles < 200 words.
    - [ ] Verify that tests fail as expected (Red Phase).
- [ ] Task: Implement word count check in the dev.to ingestion logic
    - [ ] Update `app/services/connectors/devto.py` (or relevant ingestion path) to calculate word count.
    - [ ] Skip articles under 200 words and log the skip.
    - [ ] Verify that all unit tests pass (Green Phase).
- [ ] Task: Conductor - User Manual Verification 'dev.to Quickie Filtering' (Protocol in workflow.md)

## Phase 3: Documentation & Final Verification
This phase focuses on ensuring the project's documentation is up-to-date and all changes are verified across the suite.

- [ ] Task: Update project documentation
    - [ ] Update `docs/design-and-walkthrough.md` with details on the new ingestion logic and filtering.
    - [ ] Update `docs/testing.md` with descriptions of the new tests added in this track.
- [ ] Task: Final Verification and Coverage
    - [ ] Run all unit and integration tests: `make test`.
    - [ ] Check code coverage for modified modules: `uv run pytest --cov=app/tools --cov=app/services/connectors`.
- [ ] Task: Conductor - User Manual Verification 'Documentation & Final Verification' (Protocol in workflow.md)
