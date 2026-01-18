# Track Specification: Containerisation & Origin Unified Backend

## Overview
This track focuses on productionising the Dazbo Portfolio deployment by unifying the frontend and backend into a single, multi-stage container image. We will adopt a "Unified Origin" architecture where FastAPI serves both the API and the static React assets. This simplifies deployment, eliminates CORS complexity in production, and provides a clean separation of concerns via the `/api` prefix.

## Functional Requirements
- **Multi-stage Docker Build**:
    - **Stage 1 (Frontend)**: Use Node.js (LTS) to build the React application into static assets.
    - **Stage 2 (Final)**: Use the existing Python 3.12 environment. Copy the frontend assets from Stage 1 and the backend code.
- **API Restructuring**:
    - Prefix all existing backend routes (`/projects`, `/blogs`, `/experience`, `/feedback`) with `/api`.
    - Update the frontend `contentService.ts` and `vite.config.ts` to reflect the new `/api` pathing.
- **Static File Serving**:
    - Configure FastAPI to serve the React `dist` directory.
    - Implement a "catch-all" route to serve `index.html` for any non-API path, allowing React Router to manage client-side navigation.
- **Documentation & Tooling Update**:
    - **`README.md`**: Add instructions for running the unified container locally and differentiate between raw process dev vs container dev.
    - **`Makefile`**: Add `docker-build` and `docker-run` targets. Update existing targets if their behavior changes.
    - **`docs/design-and-walkthrough.md`**: 
        - Add "Unified Origin Architecture" design decision and rationale.
        - Add "CORS Strategy" section explaining the Same-Origin Policy in production vs Proxy in development.
        - Add a thorough technical walkthrough of the frontend UI implementation (component structure, styling strategy).

## Design Decisions & Rationale
- **Single Container vs Sidecar**: Choosing Single Container for Cloud Run to minimize operational complexity and cost.
- **Unified Origin**: Serving React from FastAPI avoids the need for CORS configuration in production and simplifies SSL/Domain management.
- **API Prefixing**: `/api` ensures no collisions between frontend client-side routes and backend endpoints.

## CORS Strategy
- **Production**: None required (Same-origin).
- **Local Development**: Maintain Vite proxy (`:5173` -> `:8000`) to mirror production origin-sharing behavior without relaxing backend security headers.

## Acceptance Criteria
- [ ] Docker image builds successfully and includes both compiled frontend and backend code.
- [ ] Running the container locally (port 8080) allows accessing the UI at `/` and API at `/api`.
- [ ] Frontend successfully fetches data from the backend via the `/api` prefixed routes within the container.
- [ ] Navigation (e.g., refreshing a `/details/123` page) works correctly via the FastAPI catch-all handler.
- [ ] All specified documents are updated with accurate architectural details and run instructions.

## Out of Scope
- Implementing side-car or multi-container deployments.
- CI/CD pipeline updates (to be handled in a separate infrastructure track if needed).
