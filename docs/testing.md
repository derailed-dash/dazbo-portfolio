# Testing & Quality Assurance

This project uses a comprehensive suite of tools to ensure code quality and functionality.

## Tooling

*   **Test Runner**: `pytest` is used for running all tests.
*   **Package Manager**: `uv` handles dependency management and virtual environments.
*   **Linting & Formatting**:
    *   `ruff`: Handles Python linting (imports, complexity, PEP compliance) and auto-formatting.
    *   `codespell`: Checks for common spelling errors.
    *   `ty`: Performs static type checking (similar to mypy/pyright).

## Commands

*   `make test`: Runs unit and integration tests with warnings suppressed.
*   `make lint`: Runs the full suite of code quality checks (codespell, ruff, ty).

## Unit Tests

Located in `tests/unit/`.

Unit tests focus on isolating individual components, particularly Models and Services.

*   **Models**: Verify Pydantic validation logic and defaults (e.g., `tests/unit/test_models.py`).
*   **Services**: Test business logic without connecting to external services. We use `unittest.mock` to mock the `google.cloud.firestore.AsyncClient` and other dependencies to ensure tests are fast and deterministic.
*   **Adherence to Standards**: Tests like `test_firestore_session_service_implements_base` ensure that our implementations correctly follow required interfaces (e.g., Google ADK).

## Integration Tests

Located in `tests/integration/`.

Integration tests verify the interaction between components, primarily focusing on the FastAPI endpoints and the Agent runtime.

### API Endpoints (`test_endpoints.py`)
These tests verify that the API routes return the correct status codes and data structures.
*   **Mocking Strategy**: To avoid dependencies on a live Firestore database during testing, we use FastAPI's `dependency_overrides`.
    *   We override the service dependencies (e.g., `get_project_service`) in the `app` instance.
    *   These overrides provide `AsyncMock` objects that simulate Service responses.
    *   This ensures we test the *API Layer* (routing, serialization) without the *Data Layer* (network calls, DB state).

### Agent & Server (`test_agent.py`, `test_server_e2e.py`)
*   **Agent Logic**: Verifies that the Agent can process inputs and generate responses using the configured tools and prompt.
*   **E2E Server**: Tests the full server stack, including Server-Sent Events (SSE) for streaming agent responses.
