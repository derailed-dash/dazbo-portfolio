# Plan: Firestore Migration and Schema Definition

## Phase 1: Foundation & Configuration [checkpoint: 63a5568]
- [x] Task: Add `google-cloud-firestore` to dependencies in `pyproject.toml` [1f358fd]
- [x] Task: Update environment configuration in `app/config.py` (if exists) and `.env.template` to support Firestore settings (Project ID, Database ID) [89f33d2]
- [x] Task: Conductor - User Manual Verification 'Foundation & Configuration' (Protocol in workflow.md)

## Phase 2: Data Schema & Service Implementation [checkpoint: 1c83e8a]
- [x] Task: Define Pydantic models for `Project`, `Blog`, and `Experience` in `app/models/` [f037867]
- [x] Task: Implement `FirestoreService` base class in `app/services/firestore_base.py` [850ebea]
- [x] Task: Implement specific services for `Project`, `Blog`, and `Experience` in `app/services/` [116f320]
- [x] Task: Implement `FirestoreSessionService` for ADK in `app/services/session_service.py` [6367329]
- [x] Task: Conductor - User Manual Verification 'Data Schema & Service Implementation' (Protocol in workflow.md)

## Phase 3: Integration & Clean-up [checkpoint: 71d2b32]
- [x] Task: Update FastAPI dependency injection in `app/fast_api_app.py` to use Firestore services [0e1964c]
- [x] Task: Update API endpoints in `app/fast_api_app.py` to utilize new Firestore service methods [252cf15]
- [x] Task: Remove `asyncpg` dependency and delete any residual PostgreSQL-specific code (e.g., `deployment/terraform/sql/`) [a379fb8]
- [x] Task: Update `tech-stack.md` to reflect the final database implementation [f05051a]
- [x] Task: Conductor - User Manual Verification 'Integration & Clean-up' (Protocol in workflow.md)
