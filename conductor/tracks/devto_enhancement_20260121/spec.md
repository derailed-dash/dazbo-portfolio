# Track Specification: Enhance Dev.to Ingestion (Filter & Enrich)

## Overview
This track aims to improve the quality of blog posts ingested from Dev.to. Currently, the ingestion process indiscriminately fetches all posts and lacks the AI-powered enrichment (summaries and tagging) applied to Medium posts. This results in "low-value" content (like "Quickie" posts) appearing in the portfolio and inconsistent metadata compared to other sources.

## Functional Requirements

### 1. Filter "Quickie" Posts
- **Logic:** The `DevToConnector` must filter out posts based on their title.
- **Criteria:** Exclude any post where the `title` starts with the string `[Boost]`.
- **Logging:** Log a "Skipping (quickie)" message for any post excluded by this filter.

### 2. Enable AI Enrichment for Dev.to
- **Integration:** Integrate the `ContentEnrichmentService` into the `DevToConnector` workflow.
- **Trigger:** For every valid (non-skipped) Dev.to post, trigger the enrichment process.
- **Outputs:**
    - Generate a technical summary (no more than 225 words).
    - Generate 5 relevant technical tags.
    - **Fallback:** If AI generation fails, fallback to the original description and tags provided by the Dev.to API.

### 3. Retrieve and Store Markdown Content
- **Source:** Use the Dev.to API to retrieve the article's content.
- **Format:** Prefer the original Markdown (`body_markdown`) from the API if available, as Dev.to native format is already Markdown.
- **Storage:** Populate the `markdown_content` field of the `Blog` model with this data.

## Non-Functional Requirements
- **Consistency:** The data structure for Dev.to blogs in Firestore must match that of Medium blogs (specifically `ai_summary`, `markdown_content`, and `tags`).
- **Performance:** Ingestion time will increase due to LLM calls. Ensure appropriate logging/progress feedback is maintained (e.g., "Enriching content...").
- **Error Handling:** If the AI service is unavailable, the ingestion should complete with the basic metadata rather than failing the entire batch.

## Acceptance Criteria
- [ ] Posts with titles starting with `[Boost]` are NOT saved to Firestore.
- [ ] Ingested Dev.to blogs have a populated `ai_summary` field in Firestore.
- [ ] Ingested Dev.to blogs have a populated `markdown_content` field in Firestore.
- [ ] Ingested Dev.to blogs have a populated `tags` list (enhanced or original).
- [ ] The ingestion CLI output indicates which posts were skipped.

## Out of Scope
- Enhancing GitHub or Manual YAML ingestion sources.
- Retroactive cleanup of *existing* Firestore records (this spec covers the ingestion logic; re-running the tool will update them).
