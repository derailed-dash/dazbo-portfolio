# Specification: Replacement and Deletion of Video Entries

## Overview
This track enhances the `app/tools/ingest.py` tool to handle updates and deletions of video resources more intelligently. Currently, ingestion primarily adds or updates based on specific triggers; this enhancement introduces interactive verification for replacing existing videos (where titles match but URLs differ) and removing videos that are no longer present in the manual source.

## Functional Requirements
1. **Intelligent Video Matching**:
   - The tool must check for existing videos using both **Video Title** and **Video URL**.
   - **Replacement Detection**: If a video in the YAML source shares a title with an existing Firestore entry but has a different URL, it should be flagged as a potential replacement.
   - **Title Update Detection**: If a video shares a URL but has a different title, it should be flagged as a title update.
2. **Interactive CLI Prompts**:
   - For every detected replacement or significant update, the tool must pause and prompt the user for confirmation (e.g., `Update video 'Title' [y/N]?`).
   - For every video found in Firestore (marked as manual/YAML source) that is **not** present in the current YAML source file, the tool must prompt the user for deletion.
3. **In-place Updates**:
   - Confirmed replacements and updates must modify the existing Firestore document in-place, preserving its document ID where appropriate, rather than creating duplicates.
   - All fields (description, tags, publish date, etc.) are eligible for overwriting during an update.
4. **Scoped Deletion**:
   - Deletion checks are strictly limited to videos originally ingested via the manual YAML process (where `is_manual: true` or `source_platform: "manual"`).

## Non-Functional Requirements
- **Determinism**: The logic for detecting "missing" entries must be robust against accidental deletions (e.g., ensuring the YAML was correctly loaded).
- **User Experience**: Prompts should be clear and provide enough context (e.g., showing the old vs. new URL) for the user to make an informed decision.

## Acceptance Criteria
- Running `ingest.py` with a modified URL for an existing title prompts for update and, if confirmed, updates the record without duplicating it.
- Running `ingest.py` after removing a video from the YAML source prompts for its deletion from Firestore.
- Deleting or updating one video does not affect other video entries or blog/project resources.
- Simulation mode (`--simulate`) correctly displays these proposed interactive actions without executing them.

## Out of Scope
- Automated synchronization of non-manual video sources (e.g., direct YouTube API sync) beyond existing logic.
- Bulk auto-deletion without user interaction.
