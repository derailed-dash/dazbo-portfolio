# Specification: YouTube Content Ingestion (Manual)

## Overview
This track involves implementing a system to manually specify YouTube videos in the existing `manual_applications.yaml.enc` (or a similar YAML file) and ingest them into the portfolio. The goal is to showcase specific video content (tutorials, presentations, etc.) on the home page through a new dedicated carousel.

## Functional Requirements
- **Manual Ingestion Enhancement:** The `ingest` tool must support a new "Videos" section in the manual YAML file to specify YouTube video details.
- **Manual Metadata:** The user will provide all video metadata (title, description, thumbnail_url, publish_date, video_url) in the YAML file.
- **Firestore Schema:** Store the video records in a new `videos` collection, following the platform-scoped ID pattern (e.g., `youtube:<video_id>`).
- **UI Carousel:** Implement a new `ShowcaseCarousel` on the React frontend to display the ingested videos.
- **Documentation:** Update `docs/design-and-walkthrough.md` with example YAML entries for the new "Videos" section.

## Acceptance Criteria
- [ ] The `ingest` tool successfully parses the new "Videos" section in the manual YAML file and saves them to Firestore.
- [ ] Ingested videos appear correctly in a new "Videos" carousel on the portfolio home page.
- [ ] Video cards include title, manual description, and clickable thumbnail linking to YouTube.
- [ ] `docs/design-and-walkthrough.md` contains clear examples for the new YAML structure.

## Out of Scope
- Automated metadata fetching via YouTube API.
- AI summarization or transcript extraction.
