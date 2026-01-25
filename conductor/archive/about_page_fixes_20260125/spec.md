# Track Specification: About Page Fixes and Agent Integration

## Overview
This track addresses issues with the "About" page where Markdown is not rendering correctly as HTML and content does not appear to update on page refresh. Additionally, it extends the Chatbot's capabilities to allow it to retrieve the "About" content from Firestore, enabling it to answer questions about the portfolio owner's professional background.

## Functional Requirements
### Frontend (About Page)
1.  **Markdown Rendering**: Verify and fix the `AboutPage` component to ensure it correctly renders Markdown content from the `body` field of the Firestore `content/about` document.
2.  **Content Fetching**: Ensure the `AboutPage` fetches the latest content from the `/api/content/about` endpoint on every component mount (page refresh).

### Backend (Agent & Tools)
1.  **Agent Tooling**: Update the `get_content_details` tool to support retrieving documents from the `content` collection. Specifically, it should be able to fetch the `about` document.
2.  **Agent Search**: (Optional but recommended) Update `portfolio_search` to include the `content` collection if relevant queries are made.

## Non-Functional Requirements
- **Performance**: Fetching content from Firestore should remain efficient and not block the UI (use existing loading states).
- **Consistency**: The Chatbot should use the same source of truth (Firestore) as the frontend.

## Acceptance Criteria
- The "About" page correctly renders Markdown (e.g., headings, bold text, lists).
- Updating the `body` field in the Firestore `about` document and refreshing the "About" page reflects the changes immediately.
- The Chatbot can answer "Who are you?" or "Tell me about yourself" by invoking a tool to retrieve the `about` content.

## Out of Scope
- Real-time Firestore subscriptions (Simple fetch-on-mount is sufficient).
- Implementation of Vector Search (RAG).
