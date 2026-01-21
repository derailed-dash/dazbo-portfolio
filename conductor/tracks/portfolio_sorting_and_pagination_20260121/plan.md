# Implementation Plan: Portfolio Sorting and Mobile Pagination Fix

## Phase 1: Backend Sorting Logic
Refine the service layer to ensure all portfolio data is returned in reverse chronological order (newest first).

- [x] Task: Update `BlogService` to sort by date descending 509c20e
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns blogs sorted by date (newest first).
    - [ ] Modify `app/services/blog_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [x] Task: Update `ProjectService` to sort by date descending 03e77ce
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns projects sorted by date (newest first).
    - [ ] Modify `app/services/project_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [x] Task: Update `ExperienceService` to sort by date descending f5be639
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns experience entries sorted by date (newest first).
    - [ ] Modify `app/services/experience_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [x] Task: Conductor - User Manual Verification 'Backend Sorting Logic' (Protocol in workflow.md) [checkpoint: 779793d]

## Phase 2: Frontend Carousel Pagination Fix
Modify the `ShowcaseCarousel` component to handle high page counts on mobile by limiting visible indicators.

- [x] Task: Implement Limited Pagination Indicators in `ShowcaseCarousel` 0af2ae3
    - [x] Create/Update frontend unit test for `ShowcaseCarousel` to verify that indicators are limited on mobile when page count is high.
    - [x] Modify `frontend/src/components/ShowcaseCarousel.tsx` to implement a "sliding window" or limited dot logic for mobile view.
    - [x] Ensure CSS handles the new indicator style gracefully.
    - [x] Run frontend tests and verify "Green" phase.
- [x] Task: Verify Responsive Behavior 0af2ae3
    - [x] Verify that the desktop view still shows all indicators (or remains unaffected).
    - [x] Verify that swipe and arrow navigation still update the (limited) indicators correctly on mobile.
- [x] Task: Conductor - User Manual Verification 'Frontend Carousel Pagination Fix' (Protocol in workflow.md) [checkpoint: 2ee0af7]

## Phase 3: Final Integration and Quality Gate
Final verification of the combined fixes.

- [x] Task: Fix `GitHubConnector` to map `created_at` field 3316c9c
    - [x] Modify `app/services/connectors/github_connector.py` to map `created_at` or `pushed_at` from GitHub API.
    - [x] Create/Update test to verify mapping.
- [ ] Task: End-to-End Verification
    - [ ] Run all integration tests `make test`.
    - [ ] Run all linting and quality checks `make lint`.
    - [ ] Verify sorting across all sections in the live UI (using `make react-ui` and `make local-backend`).
- [ ] Task: Conductor - User Manual Verification 'Final Integration and Quality Gate' (Protocol in workflow.md)
