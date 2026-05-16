# Implementation Plan: Video Ingestion Sync

## Phase 1: Research and TDD for Sync Logic
- [ ] Task: Analyze `_process_manual_videos` in `app/tools/ingest.py` for extension points.
- [ ] Task: Create `tests/unit/test_ingest_videos_sync.py` with failing tests for:
    - [ ] Detecting video replacement (Title matches, URL differs).
    - [ ] Detecting title updates (URL matches, Title differs).
    - [ ] Detecting missing manual entries in YAML that exist in Firestore.
    - [ ] Verifying simulation mode (`--simulate`) behavior for these scenarios.
- [ ] Task: Conductor - User Manual Verification 'Research and TDD' (Protocol in workflow.md)

## Phase 2: Core Matching and Detection Logic
- [ ] Task: Refactor `_process_manual_videos` to support multi-key matching (Title + URL).
- [ ] Task: Implement deletion detection logic to identify "stale" manual videos in Firestore.
- [ ] Task: Update logic to support `--simulate` by logging proposed sync actions.
- [ ] Task: Verify that all new unit tests pass (Green phase).
- [ ] Task: Conductor - User Manual Verification 'Core Detection Logic' (Protocol in workflow.md)

## Phase 3: Interactive CLI Prompts
- [ ] Task: Implement asynchronous-friendly interactive prompts for:
    - [ ] Confirming video replacement/update.
    - [ ] Confirming video deletion.
- [ ] Task: Ensure prompts are skipped when `--simulate` is active or in non-interactive environments.
- [ ] Task: Update `_process_manual_videos` to utilize these prompts.
- [ ] Task: Conductor - User Manual Verification 'Interactive Prompts' (Protocol in workflow.md)

## Phase 4: Integration and Final Quality Check
- [ ] Task: Run full ingestion suite tests (`tests/unit/test_ingest_*.py`) to ensure no regressions.
- [ ] Task: Perform manual verification using `sample_data/manual_videos.yaml` with additions, removals, and URL changes.
- [ ] Task: Review and update `docs/architecture-and-walkthrough.md` to reflect ingestion tool improvements.
- [ ] Task: Run `ruff` and `codespell` to ensure code quality.
- [ ] Task: Conductor - User Manual Verification 'Integration and Quality Check' (Protocol in workflow.md)
