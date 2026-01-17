# Plan: Firestore Migration and Schema Definition

## Phase 1: Foundation & Configuration
- [x] Task: Add `google-cloud-firestore` to dependencies in `pyproject.toml` [1f358fd]
- [ ] Task: Update environment configuration in `app/config.py` (if exists) and `.env.template` to support Firestore settings (Project ID, Database ID)
- [ ] Task: Conductor - User Manual Verification 'Foundation & Configuration' (Protocol in workflow.md)

## Phase 2: Data Schema & Service Implementation
- [ ] Task: Define Pydantic models for `Project`, `Blog`, and `Experience` in `app/models/`
- [ ] Task: Implement `FirestoreService` base class in `app/services/firestore_base.py`
- [ ] Task: Implement specific services for `Project`, `Blog`, and `Experience` in `app/services/`
- [ ] Task: Implement `FirestoreSessionService` for ADK in `app/services/session_service.py`
- [ ] Task: Conductor - User Manual Verification 'Data Schema & Service Implementation' (Protocol in workflow.md)

## Phase 3: Integration & Clean-up
- [ ] Task: Update FastAPI dependency injection in `app/fast_api_app.py` to use Firestore services
- [ ] Task: Update API endpoints in `app/fast_api_app.py` to utilize new Firestore service methods
- [ ] Task: Remove `asyncpg` dependency and delete any residual PostgreSQL-specific code (e.g., `deployment/terraform/sql/`)
- [ ] Task: Update `tech-stack.md` to reflect the final database implementation
- [ ] Task: Conductor - User Manual Verification 'Integration & Clean-up' (Protocol in workflow.md)
