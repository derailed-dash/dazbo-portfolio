# Implementation Plan - Rate Limiting for Cost & DoS Control

This plan outlines the steps to integrate `slowapi` for backend rate limiting and update the React frontend to handle rate limit errors gracefully.

## Phase 1: Backend Rate Limiting Implementation [checkpoint: b761624]
- [x] Task: Integrate `slowapi` and Configure Global Limits [commit: ee488fc]
    - [x] Add `slowapi` to `pyproject.toml` dependencies
    - [x] Write unit/integration tests for global rate limiting in `tests/integration/test_endpoints.py`
    - [x] Initialize `Limiter` and add `SlowAPI` middleware in `app/fast_api_app.py`
    - [x] Apply baseline limit (60/minute) to all `/api` routes
- [x] Task: Implement Strict Agent Limits [commit: 524a6b7]
    - [x] Write integration tests for chat endpoint rate limiting in `tests/integration/test_chat_endpoint.py`
    - [x] Apply strict limit (5/minute) specifically to the chat/SSE endpoint
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend Rate Limiting' (Protocol in workflow.md) [commit: b761624]

## Phase 2: Frontend Error Handling
- [~] Task: Handle 429 in Chat Widget
    - [ ] Write Vitest tests for `ChatWidget` error state handling
    - [ ] Update `frontend/src/components/ChatWidget.tsx` to detect 429 status and display a friendly "Please wait" message
- [ ] Task: Global API Error Handling
    - [ ] Update frontend API services/interceptors to handle 429 status (e.g., via console warnings or toast notifications)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Error Handling' (Protocol in workflow.md)

## Phase 3: Documentation & Verification
- [ ] Task: Update Design and Walkthrough Documentation
    - [ ] Add "In-Memory Rate Limiting" to Design Decisions table in `docs/design-and-walkthrough.md`
    - [ ] Add a section explaining the rate limiting architecture and frontend feedback loop
- [ ] Task: Final Quality Gate & Verification
    - [ ] Run all project tests (`make test`) and verify coverage
    - [ ] Run `make lint` to ensure code style compliance
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Documentation & Finalization' (Protocol in workflow.md)
