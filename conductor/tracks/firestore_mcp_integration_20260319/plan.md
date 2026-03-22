# Implementation Plan: `firestore_mcp_integration`

## Phase 1: Infrastructure and Permissions [checkpoint: cd22a24]
- [x] Task: Update Terraform to enable Firestore API and assign roles
    - [x] Add `firestore.googleapis.com` to the enabled APIs list in `deployment/terraform/apis.tf`.
    - [x] Add `roles/mcp.toolUser` and `roles/datastore.user` to the application service account roles in `deployment/terraform/iam.tf`.
- [x] Task: Enable Firestore MCP server via script or Terraform
    - [x] Ensure the Firestore remote MCP server is enabled (using `gcloud beta services mcp enable firestore.googleapis.com`).
- [x] Task: Verify Infrastructure Deployment
    - [x] Run `make tf-plan` to verify the changes.
    - [x] Run `make tf-apply` to deploy the changes.
- [x] Task: Conductor - User Manual Verification 'Infrastructure and Permissions' (Protocol in workflow.md)

## Phase 2: Agent Integration and Testing
- [x] Task: Update `app/agent.py` to integrate Firestore MCP
    - [x] Import `McpToolset` from `google.adk.tools.mcp_tool`.
    - [x] Import `SseConnectionParams` from `google.adk.tools.mcp_tool.mcp_session_manager` (or equivalent for HTTP/SSE as per ADK docs).
    - [x] Initialize `McpToolset` with `https://firestore.googleapis.com/mcp`.
    - [x] Configure `tool_filter` to include `list_documents`, `get_document`, and `list_collections`.
    - [x] Update `root_agent` to use the new `McpToolset`.
    - [x] Remove manual imports and registrations for `search_portfolio` and `get_content_details`.
- [x] Task: Refine Agent Instructions for MCP Tools
    - [x] Update `instruction` in `root_agent` to guide the agent on how to use Firestore MCP tools (e.g., searching in `projects`, `blogs`, and `content` collections).
    - [x] Specifically instruct the agent to look for `item_id: 'about'` in the `content` collection for "About Me" queries using `get_document`.
- [x] Task: Write Integration Tests for MCP Integration
    - [x] Create `tests/integration/test_firestore_mcp_agent.py`.
    - [x] Write tests to confirm the agent can:
        - [x] List documents in `projects` and `blogs` collections.
        - [x] Retrieve the `about` document from the `content` collection.
        - [x] Search for specific content using natural language (leveraging the agent's ability to call the right MCP tools).
- [x] Task: Verify Agent Functionality
    - [x] Run `make test` to ensure the agent functions correctly with the new MCP integration.
    - [x] Manually verify chat interaction using `make playground`.
- [x] Task: Conductor - User Manual Verification 'Agent Integration and Testing' (Protocol in workflow.md)

## Phase 3: Code Cleanup and Documentation (Hybrid Approach)
- [ ] Task: Delete Obsolete Custom Tools
    - [ ] Remove `app/tools/content_details.py`.
    - [ ] **NOTE**: `app/tools/portfolio_search.py` is RETAINED as part of the Hybrid Architecture for context-efficient discovery.
- [ ] Task: Update Design and Walkthrough Documentation
    - [ ] Update `docs/design-and-walkthrough.md` to reflect the move to a managed MCP server.
    - [ ] **NEW**: Add a dedicated section explaining the **Hybrid Tooling Rationale** (Bespoke Search + MCP Retrieval).
- [ ] Task: Update Deployment Documentation
    - [ ] Update `deployment/README.md` with instructions for enabling and verifying the Firestore MCP server.
- [ ] Task: Final Verification and Checkpoint
    - [ ] Run `make lint` and `make test` to ensure the project is in a clean state.
- [ ] Task: Conductor - User Manual Verification 'Code Cleanup and Documentation' (Protocol in workflow.md)

## Phase 4: Migration Blog Post
- [ ] Task: Create and Update Migration Journey Blog Post
    - [ ] Create `docs/blog_migration_journey.md` as a basis for the Dazbo style blog.
    - [ ] Document the initial state (custom Firestore tools).
    - [ ] Document the transition to Firestore MCP (Phase 1 & 2).
    - [ ] Document the benefits observed (e.g., reduced code maintenance, standard protocol).
    - [ ] **NEW**: Document the discovery of the schema bug and the implementation of the Monkey-Patch.
    - [ ] **NEW**: Document the pivot to a **Hybrid Architecture** and why it's better than pure MCP.
    - [ ] Update the blog post as implementation progresses.
- [ ] Task: Final Quality Check for Blog Completeness
    - [ ] **NEW**: Review the final blog post for technical accuracy, persona consistency (Dazbo style), and coverage of all key implementation hurdles.
- [ ] Task: Conductor - User Manual Verification 'Migration Blog Post' (Protocol in workflow.md)
