# Implementation Plan: Portfolio Sorting and Mobile Pagination Fix

## Phase 1: Backend Sorting Logic
Refine the service layer to ensure all portfolio data is returned in reverse chronological order (newest first).

- [x] Task: Update `BlogService` to sort by date descending 509c20e
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns blogs sorted by date (newest first).
    - [ ] Modify `app/services/blog_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [ ] Task: Update `ProjectService` to sort by date descending
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns projects sorted by date (newest first).
    - [ ] Modify `app/services/project_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [ ] Task: Update `ExperienceService` to sort by date descending
    - [ ] Create/Update unit test in `tests/unit/test_services.py` to verify `list` returns experience entries sorted by date (newest first).
    - [ ] Modify `app/services/experience_service.py` to include sorting in the Firestore query.
    - [ ] Run tests and verify "Green" phase.
- [ ] Task: Conductor - User Manual Verification 'Backend Sorting Logic' (Protocol in workflow.md)

## Phase 2: Frontend Carousel Pagination Fix
Modify the `ShowcaseCarousel` component to handle high page counts on mobile by limiting visible indicators.

- [ ] Task: Implement Limited Pagination Indicators in `ShowcaseCarousel`
    - [ ] Create/Update frontend unit test for `ShowcaseCarousel` to verify that indicators are limited on mobile when page count is high.
    - [ ] Modify `frontend/src/components/ShowcaseCarousel.tsx` to implement a "sliding window" or limited dot logic for mobile view.
    - [ ] Ensure CSS handles the new indicator style gracefully.
    - [ ] Run frontend tests and verify "Green" phase.
- [ ] Task: Verify Responsive Behavior
    - [ ] Verify that the desktop view still shows all indicators (or remains unaffected).
    - [ ] Verify that swipe and arrow navigation still update the (limited) indicators correctly on mobile.
- [ ] Task: Conductor - User Manual Verification 'Frontend Carousel Pagination Fix' (Protocol in workflow.md)

## Phase 3: Final Integration and Quality Gate
Final verification of the combined fixes.

- [ ] Task: End-to-End Verification
    - [ ] Run all integration tests `make test`.
    - [ ] Run all linting and quality checks `make lint`.
    - [ ] Verify sorting across all sections in the live UI (using `make react-ui` and `make local-backend`).
- [ ] Task: Conductor - User Manual Verification 'Final Integration and Quality Gate' (Protocol in workflow.md)
