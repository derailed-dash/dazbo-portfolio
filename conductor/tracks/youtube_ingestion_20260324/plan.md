# Implementation Plan: YouTube Content Ingestion (Manual)

## Phase 1: Backend Implementation (Models, Services, Ingestion)
- [x] Task: Create `app/models/video.py` [1920c2b]
    - [x] Define `Video` Pydantic model with fields: `id`, `title`, `description`, `thumbnail_url`, `publish_date`, `video_url`, `is_manual`, `source_platform`.
- [x] Task: Create `app/services/video_service.py` [8482659]
    - [x] Implement `VideoService` inheriting from `FirestoreService[Video]`.
- [x] Task: Update `app/tools/ingest.py` [c57daf6, f706a89]
    - [x] Import `Video` and `VideoService`.
    - [x] Update `ingest_resources` to initialize `VideoService`.
    - [x] Update the YAML processing logic to handle a new `videos` key.
    - [x] Add helper logic to process manual video entries.
    - [x] Refactor helpers to correctly track and display ingestion summary stats.
- [x] Task: Write Tests for Video Ingestion [c57daf6]
    - [x] Create `tests/unit/test_ingest_videos.py` to verify YAML parsing and Firestore saving.
    - [x] Create `tests/unit/test_video_model.py` for schema validation.
- [x] Task: Conductor - User Manual Verification 'Backend Implementation' (Protocol in workflow.md) [checkpoint: 1ca7305]

## Phase 2: Frontend Implementation (Service & UI)
- [x] Task: Create `frontend/src/services/videoService.ts` [7a9e61d]
    - [x] Implement `getVideos` to fetch from `/api/videos`.
- [~] Task: Add Backend API Route for Videos
    - [ ] Update `app/fast_api_app.py` to include a GET `/api/videos` endpoint using `VideoService`.
- [ ] Task: Update `frontend/src/pages/HomePage.tsx`
    - [ ] Fetch videos on component mount.
    - [ ] Implement a new `ShowcaseCarousel` for "Videos".
    - [ ] Ensure the carousel is responsive and matches the existing design.
- [ ] Task: Write Tests for Videos Carousel
    - [ ] Create tests to verify the new carousel renders correctly with video data.
- [ ] Task: Conductor - User Manual Verification 'Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Documentation & Finalization
- [ ] Task: Update `docs/design-and-walkthrough.md`
    - [ ] Add example YAML entries for the `videos` section.
- [ ] Task: Final Check and Checkpoint
    - [ ] Run `make lint` and `make test`.
- [ ] Task: Conductor - User Manual Verification 'Documentation & Finalization' (Protocol in workflow.md)
