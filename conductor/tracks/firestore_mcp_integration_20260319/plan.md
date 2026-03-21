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
- [ ] Task: Update `app/agent.py` to integrate Firestore MCP
    - [ ] Import `McpToolset` from `google.adk.tools.mcp_tool`.
    - [ ] Import `SseConnectionParams` from `google.adk.tools.mcp_tool.mcp_session_manager` (or equivalent for HTTP/SSE as per ADK docs).
    - [ ] Initialize `McpToolset` with `https://firestore.googleapis.com/mcp`.
    - [ ] Configure `tool_filter` to include `list_documents`, `get_document`, and `list_collections`.
    - [ ] Update `root_agent` to use the new `McpToolset`.
    - [ ] Remove manual imports and registrations for `search_portfolio` and `get_content_details`.
- [ ] Task: Refine Agent Instructions for MCP Tools
    - [ ] Update `instruction` in `root_agent` to guide the agent on how to use Firestore MCP tools (e.g., searching in `projects`, `blogs`, and `content` collections).
    - [ ] Specifically instruct the agent to look for `item_id: 'about'` in the `content` collection for "About Me" queries using `get_document`.
- [ ] Task: Write Integration Tests for MCP Integration
    - [ ] Create `tests/integration/test_firestore_mcp_agent.py`.
    - [ ] Write tests to confirm the agent can:
        - [ ] List documents in `projects` and `blogs` collections.
        - [ ] Retrieve the `about` document from the `content` collection.
        - [ ] Search for specific content using natural language (leveraging the agent's ability to call the right MCP tools).
- [ ] Task: Verify Agent Functionality
    - [ ] Run `make test` to ensure the agent functions correctly with the new MCP integration.
    - [ ] Manually verify chat interaction using `make playground`.
- [ ] Task: Conductor - User Manual Verification 'Agent Integration and Testing' (Protocol in workflow.md)

## Phase 3: Code Cleanup and Documentation
- [ ] Task: Delete Obsolete Custom Tools
    - [ ] Remove `app/tools/portfolio_search.py` and `app/tools/content_details.py`.
- [ ] Task: Update Design and Walkthrough Documentation
    - [ ] Update `docs/design-and-walkthrough.md` to reflect the move to a managed MCP server.
    - [ ] Add a section on the rationale for this change (simplicity, standardisation).
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
    - [ ] Update the blog post as implementation progresses.
- [ ] Task: Conductor - User Manual Verification 'Migration Blog Post' (Protocol in workflow.md)
