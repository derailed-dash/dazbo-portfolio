# Specification: Portfolio Sorting and Mobile Pagination Fix

## Overview
This track addresses two primary issues in the portfolio application:
1.  **Incorrect Sorting:** Currently, portfolio items (Projects, Blogs, Experience) are not consistently ordered by date. The requirement is to ensure the most recent items appear first (left-most in carousels, top-most in lists).
2.  **Mobile Pagination Visibility:** On mobile devices, the carousel pagination indicators (dots) for Blogs are essentially invisible because each blog post occupies a single page, leading to a high density of very small indicators.

## Functional Requirements

### 1. Unified Chronological Sorting
-   **Blogs:** Must be sorted by `date` in descending order (newest first).
-   **Projects:** Must be sorted by `date` (or equivalent timestamp) in descending order.
-   **Experience:** Must be sorted by `start_date` (or `end_date` for current roles) in descending order.
-   **Consistency:** This sorting logic should be applied at the service or API layer to ensure consistency across all views.

### 2. Improved Mobile Carousel Pagination
-   **Target:** Specifically the `ShowcaseCarousel` component when rendered on mobile devices.
-   **Logic:** Implement a mechanism to limit the number of visible pagination indicators (dots) when the page count exceeds a certain threshold (e.g., 5 or 7 dots).
-   **UX:** Users should still be able to navigate via swipe or arrows. The indicators should provide visual feedback of the current position without cluttering the UI.

## Non-Functional Requirements
-   **Performance:** Sorting should be handled efficiently, preferably at the database query level (Firestore) to minimize processing on the client.
-   **Responsiveness:** The pagination fix must specifically target mobile breakpoints without negatively impacting the desktop experience.

## Acceptance Criteria
-   [ ] Blogs carousel shows the most recent post as the first item.
-   [ ] Projects carousel shows the most recent project as the first item.
-   [ ] Experience section shows the most recent role at the top.
-   [ ] On mobile, the Blogs carousel displays a manageable number of pagination indicators (dots).
-   [ ] Carousel navigation (swipe, arrows) remains fully functional on mobile.

## Out of Scope
-   Adding new filtering or searching capabilities.
-   Modifying the desktop pagination indicator style.
