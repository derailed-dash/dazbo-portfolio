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
- [x] Task: Update `app/tools/portfolio_search.py` [c308d64]
    - [x] Import `VideoService`.
    - [x] Update `search_portfolio` to fetch and search the `videos` collection.
- [x] Task: Write Tests for Video Ingestion [c64b959]
    - [x] Create `tests/unit/test_ingest_videos.py` to verify YAML parsing and Firestore saving.
    - [x] Create `tests/unit/test_video_model.py` for schema validation.
- [x] Task: Conductor - User Manual Verification 'Backend Implementation' (Protocol in workflow.md) [checkpoint: 1ca7305]

## Phase 2: Frontend Implementation (Service & UI) [checkpoint: 3264c88]
- [x] Task: Create `frontend/src/services/videoService.ts` [7a9e61d]
    - [x] Implement `getVideos` to fetch from `/api/videos`.
- [x] Task: Add Backend API Route for Videos [662439f]
    - [x] Update `app/fast_api_app.py` to include a GET `/api/videos` endpoint using `VideoService`.
- [x] Task: Update `frontend/src/pages/HomePage.tsx` [cf559cf]
    - [x] Fetch videos on component mount.
    - [x] Implement a new `ShowcaseCarousel` for "Videos".
    - [x] Ensure the carousel is responsive and matches the existing design.
- [x] Task: Write Tests for Videos Carousel [383f1f7]
    - [x] Create tests to verify the new carousel renders correctly with video data.
- [x] Task: Conductor - User Manual Verification 'Frontend Implementation' (Protocol in workflow.md)

## Phase 3: Documentation & Finalization [checkpoint: 76154c5]
- [x] Task: Update `docs/design-and-walkthrough.md` [975fcbb]
    - [x] Add example YAML entries for the `videos` section.
- [x] Task: Final Check and Checkpoint [76154c5]
    - [x] Run `make lint` and `make test`.
- [x] Task: Conductor - User Manual Verification 'Documentation & Finalization' (Protocol in workflow.md)
