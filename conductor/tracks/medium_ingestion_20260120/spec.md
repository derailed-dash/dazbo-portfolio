# Specification: Comprehensive Medium Blog Ingestion

## Overview
The goal of this track is to overcome the 10-post limitation of the Medium RSS feed and enhance the portfolio's content richness. This involves a hybrid ingestion system (RSS + Zip Export), paywall detection, and a new processing pipeline that converts HTML content to structured Markdown and generates AI-powered summaries.

## Functional Requirements
- **Hybrid Ingestion Engine:**
    - Support fetching the latest 10 posts via the standard Medium RSS feed.
    - Implement a parser for Medium export archives (`posts.zip`).
    - The archive parser must extract blog metadata (title, date, content/summary, URL) from HTML files located within the `posts/` directory of the zip.
- **Content Processing & AI Enrichment:**
    - **HTML to Markdown Conversion:**
        - Convert the blog post HTML content into clean Markdown.
        - **Formatting Rules:**
            - Title: H1 (`#`)
            - Headings: H2 (`##`)
            - Subheadings: H3 (`###`)
        - **Frontmatter:** Include YAML frontmatter with `subtitle` and `tags` (if available).
    - **AI Summarization:**
        - Generate a concise summary of the entire blog post using the project's Gemini agent.
    - **Storage:** Store the generated Markdown and AI Summary in the `Blog` model in Firestore.
- **Paywall Identification:**
    - Implement heuristic analysis to detect paywalled content (e.g., "Member-only story" markers).
    - Update the `Blog` model to include a `is_private` boolean field.
- **Duplicate Management & Idempotency:**
    - Detect duplicates across RSS and Zip sources using the canonical URL (fallback to Title).
    - **Priority:** RSS Feed metadata takes precedence for basic fields (date, title), but the Zip export (processed into Markdown) serves as the source for the full content body.
- **CLI Enhancement:**
    - Update the `ingest` CLI tool to accept a `--medium-zip` parameter.
- **UI Presentation:**
    - Display the **AI-generated summary** in the portfolio interface.
    - Provide a clear link to the original Medium post for full reading.
    - Display a "Member-only" badge for paywalled content.

## Non-Functional Requirements
- **Performance:** Zip parsing and AI summarization should handle rate limits gracefully.
- **Maintainability:** Modular parser architecture.

## Acceptance Criteria
- [ ] Ingestion with `posts.zip` populates Firestore with historical posts.
- [ ] Blog content is stored as Markdown in Firestore (for future use/RAG).
- [ ] Each blog entry has an AI-generated summary stored in Firestore.
- [ ] The Portfolio UI displays the AI Summary and links to the full post.
- [ ] Member-only stories are correctly flagged and badged in the UI.
