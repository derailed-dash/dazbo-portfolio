# Track Specification: `firestore_mcp_integration`

## 1. Overview
The goal of this track is to replace the current custom-built Firestore search and retrieval tools with the official **Google-managed Firestore MCP server** (`firestore.googleapis.com/mcp`). This transition will leverage natural language capabilities for database interaction, simplify the codebase, and align with Google’s recommended agentic patterns.

## 2. Functional Requirements
*   **Infrastructure (Terraform):**
    *   Enable the `firestore.googleapis.com` API.
    *   Enable the Firestore MCP server using `gcloud beta services mcp enable firestore.googleapis.com` (via a null resource or direct provider support if available).
    *   Assign the `roles/mcp.toolUser` and `roles/datastore.user` IAM roles to the application's service account.
*   **Agent Configuration (ADK):**
    *   Integrate the remote MCP endpoint `https://firestore.googleapis.com/mcp` into the Gemini Agent setup.
    *   Ensure the agent can successfully call the managed tools (`list_documents`, `get_document`, etc.) using natural language prompts.
*   **Code Cleanup:**
    *   Delete `app/tools/portfolio_search.py` and `app/tools/content_details.py`.
    *   Remove any references or imports for these tools in `app/agent.py` or other parts of the application.
*   **Documentation:**
    *   Update `docs/design-and-walkthrough.md` to reflect the move to a managed MCP server.
    *   Include a rationale section in the design docs explaining the move to managed MCP (reduced maintenance, natural language query support, alignment with GCP standards).
    *   Update `deployment/README.md` with instructions for enabling and verifying the MCP server.

## 3. Non-Functional Requirements
*   **Security:** Ensure the application service account has the minimum necessary permissions to perform its tasks.
*   **Reliability:** The transition should not break existing chatbot functionality (searching blogs, projects, etc.).

## 4. Acceptance Criteria
* [ ] The Gemini Agent can answer questions about portfolio content (blogs, projects) by querying Firestore via the MCP server.
* [ ] The `portfolio_search` and `content_details` tools are removed from the repository.
* [ ] Terraform `apply` completes successfully, enabling the required APIs and roles.
* [ ] Design and deployment documentation are up-to-date.
* [ ] Rationale for the change is documented in `docs/design-and-walkthrough.md`.

## 5. Out of Scope
* Implementing write operations (Create/Update/Delete) for the chatbot (remains read-only for this phase).
* Configuring vector search or embeddings (reserved for a future track).
