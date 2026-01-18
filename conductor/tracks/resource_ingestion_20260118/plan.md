# Implementation Plan: Portfolio Resource Ingestion Strategy

## Phase 1: Foundation & Data Models [checkpoint: f36df99]
- [x] Task: Update Pydantic models to support ingestion metadata [b0319a9]
    - [ ] Add `source_platform` and `is_manual` fields to `Project` and `Blog` models
    - [ ] Add support for "metadata-only" entries
    - [ ] Update Firestore service layer to handle these new fields
- [x] Task: Verify and Update Terraform for GCS [3a306bc]
    - [ ] Check `deployment/terraform/storage.tf` for the public assets bucket definition
    - [ ] Ensure the bucket has correct public access policies (if intended for public serving)
    - [ ] Apply Terraform changes if necessary (update `tech-stack.md` if new resources are added)
- [x] Task: Implement Google Cloud Storage (GCS) Utility [3f165bb]
    - [ ] Create a utility class for uploading and retrieving URLs for images in GCS
    - [ ] Write unit tests for GCS utility with mocked storage client
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Data Models' (Protocol in workflow.md) f36df99

## Phase 2: Ingestion Connectors
- [x] Task: Implement GitHub Connector [27fec3d]
    - [ ] Create `GitHubConnector` to fetch repos using `PyGithub` or `httpx`
    - [ ] Implement mapping from GitHub API response to `Project` model
    - [ ] Write unit tests with mocked API responses
- [x] Task: Implement Medium Connector [2f860c4]
    - [ ] Create `MediumConnector` to fetch post metadata (titles, links, summaries)
    - [ ] Implement mapping to `Blog` model
    - [ ] Write unit tests with mocked responses
- [ ] Task: Implement Dev.to Connector
    - [ ] Create `DevToConnector` to fetch posts via API
    - [ ] Implement mapping to `Blog` model
    - [ ] Write unit tests with mocked API responses
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Ingestion Connectors' (Protocol in workflow.md)

## Phase 3: CLI Ingestion Tool
- [ ] Task: Implement CLI Harness
    - [ ] Create a script in `app/tools/ingest.py` using `typer` or `argparse`
    - [ ] Implement the command logic to orchestrate connectors
    - [ ] Add logic to ensure idempotency (prevent duplicates in Firestore)
- [ ] Task: Implement YAML-based Manual Entry Support
    - [ ] Define YAML schema for manual resource entries
    - [ ] Add logic to the CLI to parse YAML and insert entries into Firestore
    - [ ] Write unit tests for YAML parsing and ingestion logic
- [ ] Task: Conductor - User Manual Verification 'Phase 3: CLI Ingestion Tool' (Protocol in workflow.md)

## Phase 4: Integration & Documentation
- [ ] Task: End-to-End Integration Testing
    - [ ] Create integration tests that run the full ingestion flow against a local Firestore emulator or mock
    - [ ] Verify that images are correctly referenced and metadata is accurate
- [ ] Task: Update Documentation
    - [ ] Update `README.md` and `docs/design-and-walkthrough.md` with the new ingestion architecture
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Documentation' (Protocol in workflow.md)
