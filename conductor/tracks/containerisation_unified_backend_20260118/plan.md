# Implementation Plan - Containerisation & Origin Unified Backend

This plan outlines the steps to restructure the API, unify the frontend and backend into a single container image, and update project documentation.

## Phase 1: API Restructuring & Backend Prep
- [x] Task: Prefix FastAPI Routes with `/api`
    - [x] Update route decorators in `app/fast_api_app.py` (e.g., `@app.get("/blogs")` -> `@app.get("/api/blogs")`)
    - [x] Verify changes with existing integration tests (updating test paths as needed) [commit: f4dec56]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: API Restructuring' (Protocol in workflow.md)

## Phase 2: Frontend Alignment
- [x] Task: Update Frontend Fetching Logic
    - [x] Update `frontend/src/services/contentService.ts` to include `/api` in all requests
    - [x] Update `frontend/vite.config.ts` to proxy `/api` instead of individual endpoints [commit: 8cdf3c5]
- [x] Task: Verify Local Developer Loop
    - [x] Run `make local-backend` and `make react-ui`
    - [x] Confirm data still flows correctly through the proxy
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend Alignment' (Protocol in workflow.md)

## Phase 3: Multi-stage Container Implementation
- [x] Task: Update Dockerfile for Multi-stage Build [commit: 46d81fd]
    - [x] Add `frontend-builder` stage using Node.js to run `npm run build`
    - [x] Update final stage to copy `dist/` assets into the container
    - [x] Install any necessary Python packages for static file serving
- [x] Task: Update Makefile Tooling [commit: 46d81fd]
    - [x] Add `docker-build` target
    - [x] Add `docker-run` target (mapping port 8080)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Containerisation' (Protocol in workflow.md)

## Phase 4: Unified Origin Serving
- [x] Task: Implement FastAPI Static File Mounting
    - [x] Use `fastapi.staticfiles.StaticFiles` to serve the React `dist` directory at `/`
    - [x] Implement a catch-all Exception Handler or Route for 404s to return `index.html` (crucial for SPA navigation)
- [x] Task: Verify Unified Container Build
    - [x] Run `make docker-build` and `make docker-run`
    - [x] Access `http://localhost:8080/` and verify both UI and API work from a single port
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Unified Origin' (Protocol in workflow.md)

## Phase 5: Documentation Synchronization
- [x] Task: Update Project Documentation [commit: d8cb834]
    - [x] Update `README.md` with new unified execution instructions
    - [x] Update `docs/design-and-walkthrough.md` with architectural rationale and frontend walkthrough
- [x] Task: Conductor - User Manual Verification 'Phase 5: Documentation' (Protocol in workflow.md) [commit: 793eb44]
