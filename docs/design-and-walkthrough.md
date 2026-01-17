# Design and Walkthrough

## Design decisions:

| Decision | Rationale |
|----------|-----------|
| Use ADK for agent framework | ADK provides a solid foundation for building agents, including tools for memory, state management, and more. |
| Use Gemini for LLM | Gemini is a powerful LLM that is well-suited for this application. |
| Use FastAPI for backend | FastAPI is a modern, fast, and easy-to-use web framework for building APIs. |
| Use React for frontend | React is a popular and powerful library for building user interfaces. |
| Use Terraform for infrastructure | Terraform is a tool for defining and provisioning infrastructure as code. |
| Use Google Cloud Build for CI/CD | Google Cloud Build is a managed CI/CD service that is well-suited for this application. |
| The frontend, API and backend agent will be containerised into a single container image. | This is to simplify deployment and management. |
| The container will be deployed to Cloud Run. | Cloud Run is a fully-managed, serverless compute platform that lets you run containers directly on Google Cloud infrastructure. |
| Use FirestoreSessionService for session management | Enables persistent sessions across container restarts and scaling events, replacing the initial InMemory implementation. |
| Use Python 3.12+ Type Parameters | Leverages modern Python generic syntax (PEP 695) for cleaner and more expressive code, particularly in the Service layer. |

## Application Design

The application follows a clean, layered architecture to ensure separation of concerns and testability.

### 1. Presentation Layer (FastAPI)
*   **Entry Point**: `app/fast_api_app.py` initializes the application, configures middleware (CORS, Telemetry), and defines the lifespan context.
*   **Dependency Injection**: `app/dependencies.py` provides dependency injection providers to supply Services to Route Handlers.
*   **Routes**: API endpoints expose the functionality (e.g., `/projects`, `/blogs`, `/experience`) and Agent interaction.

### 2. Service Layer
*   **Generic Data Access**: `app/services/firestore_base.py` defines a generic `FirestoreService[T]` class. It handles common CRUD operations (create, get, list, update, delete) for any Pydantic model.
*   **Domain Services**: Specialized services (`ProjectService`, `BlogService`, `ExperienceService`) inherit from the generic base or use it to implement domain-specific logic.
*   **Session Management**: `app/services/session_service.py` implements the Google ADK's `BaseSessionService` interface using Firestore. This allows the Agent to maintain conversation state and memory persistently.

### 3. Data/Model Layer
*   **Pydantic Models**: Located in `app/models/`, these define the schema for data entities (`Project`, `Blog`, `Experience`) and ensure type safety and validation between the API and Firestore.

## Use Cases

*   **Portfolio Browsing**: Users can retrieve lists of projects, blog posts, and work experience.
*   **Agent Interaction**: Users can chat with the Gemini-powered agent to ask questions about the portfolio owner's skills and background.
