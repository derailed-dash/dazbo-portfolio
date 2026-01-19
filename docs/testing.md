# Testing & Quality Assurance

This project uses a comprehensive suite of tools to ensure code quality and functionality.

## Tooling

*   **Test Runner**: `pytest` is used for running all tests.
*   **Package Manager**: `uv` handles dependency management and virtual environments.
*   **Linting & Formatting**:
    *   `ruff`: Handles Python linting (imports, complexity, PEP compliance) and auto-formatting.
    *   `codespell`: Checks for common spelling errors.
    *   `ty`: Performs static type checking (similar to mypy/pyright).
*   **Frontend**:
    *   `Vitest`: Unit and integration test runner for React.
    *   `React Testing Library`: Testing utilities for React components.

## Commands

*   `make test`: Runs unit and integration tests with warnings suppressed.
*   `make lint`: Runs the full suite of code quality checks (codespell, ruff, ty).
*   `cd frontend && npm run test`: Runs the frontend test suite.

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

## Frontend Tests

Located in `frontend/src/`, co-located with the source files they test (e.g., `Component.tsx` -> `Component.test.tsx`).

### Components
Tests verify that UI components render correctly and handle user interactions.
*   **Rendering**: Checks that components display the expected content (e.g., `Navbar.test.tsx` checks for links).
*   **Interaction**: Simulates user events like clicking buttons or typing code.
*   **Mocking**: Uses `vi.mock` to mock child components or external libraries (like `react-router-dom`) to isolate the component under test.

### Services (`src/services/`)
Tests verify that API service modules correctly handle requests and formatting.
*   **Logic**: Checks that data transformation logic is correct.
*   **API Calls**: Uses `vi.mock('axios')` to simulate HTTP requests and ensure the correct endpoints (`/api/...`) are called.
