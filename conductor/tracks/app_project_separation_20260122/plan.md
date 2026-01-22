# Implementation Plan - Application and Project Separation

## Phase 1: Ingestion & Backend Logic
- [x] Task: Ingest Tool - Update GitHub Connector to Filter Forks [e3211c6]
    - [x] Sub-task: Modify `app/services/connectors/github_connector.py` to check the `fork` property in the GitHub API response.
    - [x] Sub-task: Add logic to skip the repository if `fork` is `true`.
- [x] Task: Ingest Tool - Add "Applications" YAML Support [680edcd]
    - [x] Sub-task: Update `app/tools/ingest.py` to parse the `applications` key from the YAML file.
    - [x] Sub-task: Implement logic to map `applications` entries to `Application` models in a separate Firestore collection.
    - [x] Sub-task: Enforce `demo_url` as a required field for `applications` entries during validation.
- [x] Task: Create Sample Applications YAML [c8b82b9]
    - [x] Sub-task: Create a file `manual_applications.yaml` (or update existing) with sample application entries (e.g., AoC Site, Portfolio).
    - [x] Sub-task: Ensure entries have valid `image_url` fields pointing to GCS placeholders or actual assets.
- [x] Task: Conductor - User Manual Verification 'Ingestion & Backend Logic'

## Phase 2: Frontend Implementation
- [x] Task: Update AppsCarousel Component [58748]
    - [x] Sub-task: Rename the component title from "Live Applications" to "Applications" in `frontend/src/components/AppsCarousel.tsx`.
    - [x] Sub-task: Remove the hardcoded mock data fallback.
    - [x] Sub-task: Update the component to fetch from the new `/api/applications` endpoint.
- [x] Task: Update ProjectCarousel Component [58748]
    - [x] Sub-task: Update `frontend/src/components/ProjectCarousel.tsx` to filter projects where `source_platform === 'github'`.
- [x] Task: Refine UI - Adjust Card Image Sizing
    - [x] Sub-task: Update `ShowcaseCard.tsx` to shrink and center images slightly for better visual balance.
- [x] Task: Conductor - User Manual Verification 'Frontend Implementation'

## Phase 3: Documentation & Verification
- [~] Task: Update Documentation
    - [ ] Sub-task: Update `docs/design-and-walkthrough.md` to document the new `applications:` YAML structure, the dedicated collection, and the fork filtering policy.
    - [ ] Sub-task: Verify the documentation example is correct.
- [ ] Task: Final Verification
    - [ ] Sub-task: Run the ingestion tool with GitHub user and YAML file.
    - [ ] Sub-task: Verify in the UI that "Applications" and "Projects" are distinct and populated correctly.
- [ ] Task: Conductor - User Manual Verification 'Documentation & Verification' (Protocol in workflow.md)
