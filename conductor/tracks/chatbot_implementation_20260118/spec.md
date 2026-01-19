# Track Specification - Chatbot Implementation

## Overview
Implement the "Dazbo" portfolio chatbot, a persistent assistant that can answer questions about the owner's professional background, projects, and blogs using a conversational Gemini-powered interface.

## User Stories
- As a visitor, I want to ask the chatbot about Dazbo's technical experience so I can understand his expertise.
- As a recruiter, I want to ask for specific project examples related to a technology (e.g., "Show me your React projects") to evaluate his skills.
- As a developer, I want to ask for blog summaries to decide which ones are worth reading.

## Functional Requirements
- **Persona Management:**
    - Retrieve the "Dazbo" persona style and system prompt from Google Secret Manager.
    - Inject the secret as an environment variable (e.g., `DAZBO_SYSTEM_PROMPT`) in Cloud Run.
- **Knowledge Retrieval:**
    - Use Direct Firestore Queries for fetching blogs and projects based on tags, titles, or metadata.
    - Implement a phased approach: Direct queries now, Vector Search (RAG) as a future enhancement.
- **Agent Tooling:**
    - `search_portfolio`: Tool to search/filter projects and blogs in Firestore.
    - `get_content_details`: Tool to retrieve full details (description, URLs) for a specific item.
- **Conversation & State:**
    - Support chat history persistence within the current session using `InMemorySessionService`.
    - Provide streaming responses via Server-Sent Events (SSE).
- **Frontend Integration:**
    - Connect the existing `ChatWidget` to the backend streaming endpoint.
    - Display message history and a "typing" state during generation.

## Technical Constraints & Decisions
- **Framework:** Google ADK and `google-genai` SDK.
- **Models:** Specified in the environment variable `MODEL`. Note that the variable `GCP_REGION` is used for the model; this is not the same as `GOOGLE_CLOUD_LOCATION` which is used for deploying resources.
- **Infrastructure:**
    - Terraform for Secret Manager resource and Cloud Run environment variable configuration.
    - Update Service Account roles to include `roles/secretmanager.secretAccessor`.
- **RAG Roadmap:** Update `TODO.md` and `docs/design-and-walkthrough.md` with instructions for future vector search implementation (Vertex AI Embeddings + Firestore Vector Search).

## Acceptance Criteria
- [ ] Agent successfully reads the system prompt from the environment variable.
- [ ] Agent can accurately answer questions about projects/blogs using tools.
- [ ] Chat history is preserved during a single session (refreshing page/reopening widget).
- [ ] Responses stream smoothly into the React UI.
- [ ] Infrastructure is updated via Terraform.

## Out of Scope
- Implementation of vector embeddings or vector search in this phase.
- Persistent session storage across container restarts (sticking with `InMemorySessionService`).