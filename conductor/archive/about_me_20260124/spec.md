# Track Specification: Professional Profile (About Me Page)

## Overview
This track implements a dedicated "About Me" page to showcase the professional bio, role, and expertise of the portfolio owner. The content will be dynamically managed via Firestore, allowing for easy updates without code changes.

## User Story
As a visitor to the portfolio, I want to read a summary of the owner's professional background and expertise so that I can understand their value proposition and experience.

## Functional Requirements
1.  **Data Layer (Firestore):**
    *   Create a new Firestore collection named `content`.
    *   Store a singleton document with ID `about`.
    *   Fields: `title` (String), `body` (Markdown String), `last_updated` (Timestamp).
2.  **Backend API (FastAPI):**
    *   Implement a GET endpoint `/api/content/{slug}` to retrieve content documents by slug.
    *   Ensure the endpoint handles missing documents gracefully (404).
3.  **Frontend (React):**
    *   **AboutPage:** Create a new page component at `/about`.
    *   **Routing:** Add the `/about` route to `App.tsx`.
    *   **Content Rendering:** Use `react-markdown` to render the `body` field from the API.
    *   **Visual Style:** Reuse the Hero banner styling for the page header to ensure visual continuity.
    *   **Navigation:** Add an "About Me" link/button in the `HeroSection` component, positioned below the profile picture.
4.  **SEO:**
    *   Integrate the `SEO` component into the `AboutPage` with appropriate metadata.

## Non-Functional Requirements
*   **Responsiveness:** The "About Me" page must be fully responsive and look good on mobile and desktop.
*   **Performance:** Content should be fetched efficiently; consider basic caching if necessary.

## Acceptance Criteria
*   The "About Me" page is accessible via the URL `/about`.
*   A link to the About page is visible and functional in the Hero section of the Homepage.
*   The content displayed on the page is fetched from the `content/about` document in Firestore.
*   Markdown formatting (bold, headers, links) in the Firestore `body` field is rendered correctly in the UI.
*   The page header matches the visual branding of the Homepage Hero banner.

## Out of Scope
*   Managing the content via a custom admin UI (manual Firestore updates via Cloud Console are sufficient).
*   Adding other profile sections like "Education" or "Skills" in this specific track (can be added to the Markdown bio).
