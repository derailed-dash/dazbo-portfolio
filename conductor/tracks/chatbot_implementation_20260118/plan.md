# Implementation Plan - Chatbot Implementation

This plan outlines the steps to implement the "Dazbo" portfolio chatbot, including backend agent logic, infrastructure updates for secret management, and frontend integration.

## Phase 1: Infrastructure & Secret Management
- [x] Task: Create Google Secret for Persona Style
    - [x] Create `dazbo-system-prompt` secret in Google Secret Manager
    - [x] Populate with the Dazbo persona and system prompt content
- [ ] Task: Update Terraform Configuration
    - [x] Define `google_secret_manager_secret` in `deployment/terraform/storage.tf` (or dedicated file)
    - [x] Update `google_cloud_run_v2_service` in `deployment/terraform/service.tf` to inject the secret as an environment variable named `DAZBO_SYSTEM_PROMPT`
    - [x] Update `app_sa_roles` in `deployment/terraform/variables.tf` to include `roles/secretmanager.secretAccessor`
- [ ] Task: Apply Infrastructure Changes
    - [ ] Run `make tf-apply` to provision resources and update Cloud Run
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure' (Protocol in workflow.md)

## Phase 2: Agent Tooling & Logic [checkpoint: 47cbdae]
- [x] Task: Implement Portfolio Search Tool [2e50bd9]
    - [x] Write unit tests for `search_portfolio` tool
    - [x] Implement `search_portfolio` in `app/agent.py` or a new tools module
    - [x] Tool should query Firestore `projects` and `blogs` collections based on query/tags
- [x] Task: Implement Content Detail Tool [b8078da]
    - [x] Write unit tests for `get_content_details` tool
    - [x] Implement `get_content_details` to fetch a full document from Firestore by ID
- [x] Task: Refine Agent Persona & System Prompt Handling [69691f7]
    - [x] Update `app/config.py` to include the environment variable name
    - [x] Modify `app/agent.py` to read the system prompt from the `DAZBO_SYSTEM_PROMPT` environment variable at runtime
    - [x] Ensure `InMemorySessionService` is correctly integrated for history persistence
- [x] Task: Conductor - User Manual Verification 'Phase 2: Agent Logic' (Protocol in workflow.md)

## Phase 3: Backend API & Streaming
- [x] Task: Implement Streaming Endpoint in FastAPI [d69d3d3]
    - [x] Write integration tests for streaming chat endpoint
    - [x] Update `app/fast_api_app.py` to include an SSE endpoint for the agent
    - [x] Ensure the agent's stream is correctly piped to the SSE response
- [x] Task: Verify Backend End-to-End
    - [x] Run `make local-backend`
    - [x] Use `curl` to verify the streaming response from the API (Verified via Integration Test `tests/integration/test_chat_endpoint.py`)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Backend Streaming' (Protocol in workflow.md)

## Phase 4: Frontend Integration
- [x] Task: Connect ChatWidget to Backend [3840ee0]
    - [x] Implement SSE listener in `frontend/src/components/ChatWidget.tsx`
    - [x] Update UI state to handle streaming chunks and display message history
    - [x] Add "typing" indicator and auto-scroll to bottom
- [~] Task: Verify UI/UX
    - [ ] Run `make react-ui` and `make local-backend`
    - [ ] Confirm chat feels responsive and correctly reflects the Dazbo persona
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Frontend Integration' (Protocol in workflow.md)

## Phase 5: Documentation & Roadmap
- [ ] Task: Update Roadmap & Design Docs
    - [ ] Append future RAG/Vector Search tasks to `TODO.md`
    - [ ] Update `docs/design-and-walkthrough.md` with the RAG roadmap details (Vertex AI + Firestore Vector Search)
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Documentation' (Protocol in workflow.md)