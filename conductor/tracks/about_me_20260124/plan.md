# Implementation Plan - Professional Profile (About Me Page)

## Phase 1: Backend Data & API
- [ ] Task: Define `Content` Pydantic model
    - [ ] Create `app/models/content.py` with `title`, `body`, and `last_updated` fields.
    - [ ] Write unit tests for the model in `tests/unit/test_models.py`.
- [ ] Task: Implement `ContentService`
    - [ ] Create `app/services/content_service.py` inheriting from `FirestoreService[Content]`.
    - [ ] Write unit tests for the service in `tests/unit/test_content_service.py`.
- [ ] Task: Add GET `/api/content/{slug}` endpoint
    - [ ] Update `app/dependencies.py` to provide `ContentService`.
    - [ ] Implement the route in `app/fast_api_app.py`.
    - [ ] Write integration tests for the endpoint in `tests/integration/test_endpoints.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend Data & API' (Protocol in workflow.md)

## Phase 2: Frontend Development
- [ ] Task: Implement Frontend `contentService`
    - [ ] Create `frontend/src/services/contentService.ts` with `getContentBySlug`.
    - [ ] Write unit tests in `frontend/src/services/contentService.test.ts`.
- [ ] Task: Create `AboutPage` component
    - [ ] Create `frontend/src/pages/AboutPage.tsx`.
    - [ ] Implement Markdown rendering using `react-markdown`.
    - [ ] Integrate the `SEO` component.
    - [ ] Write component tests in `frontend/src/pages/AboutPage.test.tsx`.
- [ ] Task: Configure Routing
    - [ ] Add the `/about` route to the main application router.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Development' (Protocol in workflow.md)

## Phase 3: UI Integration & Final Polish
- [ ] Task: Update `HeroSection` UI
    - [ ] Add an "About Me" link/button below the profile picture in `frontend/src/components/HeroSection.tsx`.
    - [ ] Style the link to be clean and integrated with the profile image area.
- [ ] Task: Refine `AboutPage` Header
    - [ ] Ensure the top of the About page uses the Hero banner styling for visual continuity.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration & Final Polish' (Protocol in workflow.md)
