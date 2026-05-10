# Specification: `deduplicate_articles`

## Overview
Deduplicate blog articles in the portfolio UI that are cross-posted on both dev.to and Medium. Instead of separate tiles, show a single tile per unique article with links to both platforms.

## Functional Requirements
- Identify duplicate articles based on an exact match of the `title` field.
- Perform deduplication on the frontend (React) during content rendering.
- When duplicates are found, merge the entries into a single object.
- Use metadata (summary, tags) from the dev.to version as the primary source.
- Display platform-specific icons at the bottom of the article tile (replacing or accompanying the standard "Read" link).
- Each icon must link to the respective article on its platform.

## Non-Functional Requirements
- Maintain fast UI rendering performance when filtering the articles list.
- Ensure icons are accessible and visually consistent with the "Midnight" theme.

## Acceptance Criteria
- Articles with identical titles from different sources appear as a single tile.
- The tile displays icons for all available platforms (dev.to and/or Medium).
- Clicking a platform icon opens the correct URL.
- Metadata (tags/summary) matches the dev.to version when both are available.

## Out of Scope
- Backend-side grouping or database schema changes.
- Fuzzy title matching or complex canonical URL logic.
