# Technology Stack

## Core Technologies

- **Language:** Python 3.12+ (Backend logic and Agent development).
- **Agent Framework:** Google Agent Development Kit (ADK) — Powers the interactive chat and agentic features.
- **Backend Framework:** FastAPI — High-performance web framework for the API layer.
- **Frontend Framework:** React 19 (with `react-markdown`) — Building the user interface for the portfolio and chat interaction. Uses **Glassmorphism** for a modern, cohesive UI aesthetic.
- **AI Enrichment:** Gemini (via `google-genai` SDK) — Powers the `ContentEnrichmentService` for technical summarisation and tagging (Medium & Dev.to).
- **Configuration:** `pydantic-settings` — Centralised and type-safe configuration management.
- **Client-Side:** `axios` (API calls), `react-router-dom` (Navigation), `lucide-react` (Icons).

## Data & Storage

- **Primary Database:** Google Firestore — Serverless, NoSQL document database for managing portfolio content and agent session data.
- **Object Storage:** Google Cloud Storage (GCS) — Storing static assets and telemetry logs.

## Infrastructure & Deployment

- **Cloud Platform:** Google Cloud Platform (GCP).
- **Compute:** Google Cloud Run — Serverless execution for the backend and frontend.
- **IaC:** Terraform — Managing cloud infrastructure as code.
- **CI/CD:** Google Cloud Build — Automated build and deployment pipelines.
- **Containerisation:** Docker — Unified container image for atomic deployments.

## Development & Quality Tools

- **Package Manager:** `uv` — Fast Python package and environment management.
- **Frontend Build Tool:** `Vite` — Modern, high-performance build tool for React.
- **Ingestion & CLI:** `typer`, `httpx`, `PyYAML`, `markdownify`, `beautifulsoup4` — Powering the hybrid resource ingestion system and HTML-to-Markdown conversion.
- **Rate Limiting:** `slowapi` — In-memory rate limiting for FastAPI.
- **Linting & Formatting:** `ruff` — Extremely fast Python linter and code formatter.
- **Testing:** `pytest` (Python), `Vitest` (React) — Feature-rich testing frameworks for unit and integration tests.
- **Quality Checks:** `codespell` (Spelling), `ty` (Static type checking), `React Testing Library` (UI verification).

## Observability

- **Telemetry:** OpenTelemetry — Instrumenting the application for traces and metrics.
- **Monitoring:** Google Cloud Trace — Visualising application latency and agent performance.
- **Logging:** Google Cloud Logging — Centralised log management.
