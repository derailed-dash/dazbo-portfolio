# Implementation Plan: `firestore_mcp_integration`

## Phase 1: Infrastructure and Permissions
- [ ] Task: Update Terraform to enable Firestore API and assign roles
    - [ ] Add `firestore.googleapis.com` to the enabled APIs list in `deployment/terraform/apis.tf`.
    - [ ] Add `roles/mcp.toolUser` and `roles/datastore.user` to the application service account roles in `deployment/terraform/iam.tf`.
- [ ] Task: Enable Firestore MCP server via script or Terraform
    - [ ] Ensure the Firestore remote MCP server is enabled (using `gcloud beta services mcp enable firestore.googleapis.com`).
- [ ] Task: Verify Infrastructure Deployment
    - [ ] Run `make tf-plan` to verify the changes.
    - [ ] Run `make tf-apply` to deploy the changes.
- [ ] Task: Conductor - User Manual Verification 'Infrastructure and Permissions' (Protocol in workflow.md)

## Phase 2: Agent Integration and Testing
- [ ] Task: Integrate Firestore MCP into Agent
    - [ ] Update `app/agent.py` to include the remote MCP endpoint `https://firestore.googleapis.com/mcp`.
    - [ ] Remove custom tool registrations for `portfolio_search` and `content_details`.
- [ ] Task: Write Integration Tests for MCP Integration
    - [ ] Create `tests/integration/test_firestore_mcp_agent.py`.
    - [ ] Write a test to confirm the agent can successfully retrieve Firestore data using the MCP tools.
- [ ] Task: Verify Agent Functionality
    - [ ] Run `make test` to ensure the agent still functions correctly with the new MCP integration.
- [ ] Task: Conductor - User Manual Verification 'Agent Integration and Testing' (Protocol in workflow.md)

## Phase 3: Code Cleanup and Documentation
- [ ] Task: Delete Obsolete Custom Tools
    - [ ] Remove `app/tools/portfolio_search.py` and `app/tools/content_details.py`.
- [ ] Task: Update Design and Walkthrough Documentation
    - [ ] Update `docs/design-and-walkthrough.md` to reflect the move to a managed MCP server.
    - [ ] Add a section on the rationale for this change.
- [ ] Task: Update Deployment Documentation
    - [ ] Update `deployment/README.md` with instructions for enabling and verifying the Firestore MCP server.
- [ ] Task: Final Verification and Checkpoint
    - [ ] Run `make lint` and `make test` to ensure the project is in a clean state.
- [ ] Task: Conductor - User Manual Verification 'Code Cleanup and Documentation' (Protocol in workflow.md)
