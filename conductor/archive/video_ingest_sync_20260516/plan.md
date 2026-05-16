# Implementation Plan: Video Ingestion Sync

## Phase 1: Research and TDD for Sync Logic [checkpoint: 3f52ff2]
- [x] Task: Analyze `_process_manual_videos` in `app/tools/ingest.py` for extension points. c223a49
- [x] Task: Create `tests/unit/test_ingest_videos_sync.py` with failing tests for: ea634b9
    - [x] Detecting video replacement (Title matches, URL differs).
    - [x] Detecting title updates (URL matches, Title differs).
    - [x] Detecting missing manual entries in YAML that exist in Firestore.
    - [x] Verifying simulation mode (`--simulate`) behavior for these scenarios.
- [x] Task: Conductor - User Manual Verification 'Research and TDD' (Protocol in workflow.md) 3f52ff2

## Phase 2: Core Matching and Detection Logic
- [x] Task: Refactor `_process_manual_videos` to support multi-key matching (Title + URL).
- [x] Task: Implement deletion detection logic to identify "stale" manual videos in Firestore.
- [x] Task: Update logic to support `--simulate` by logging proposed sync actions.
- [x] Task: Verify that all new unit tests pass (Green phase).
- [x] Task: Conductor - User Manual Verification 'Core Detection Logic' (Protocol in workflow.md)

## Phase 3: Interactive CLI Prompts
- [x] Task: Implement asynchronous-friendly interactive prompts for:
    - [x] Confirming video replacement/update.
    - [x] Confirming video deletion.
- [x] Task: Ensure prompts are skipped when `--simulate` is active or in non-interactive environments.
- [x] Task: Update `_process_manual_videos` to utilize these prompts.
- [x] Task: Conductor - User Manual Verification 'Interactive Prompts' (Protocol in workflow.md)

## Phase 4: Integration and Final Quality Check
- [x] Task: Run full ingestion suite tests (`tests/unit/test_ingest_*.py`) to ensure no regressions.
- [x] Task: Perform manual verification using `sample_data/manual_videos.yaml` with additions, removals, and URL changes.
- [x] Task: Review and update `docs/architecture-and-walkthrough.md` to reflect ingestion tool improvements.
- [x] Task: Run `ruff` and `codespell` to ensure code quality.
- [x] Task: Conductor - User Manual Verification 'Integration and Quality Check' (Protocol in workflow.md)


