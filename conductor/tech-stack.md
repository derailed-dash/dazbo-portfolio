# Technology Stack

## Core Technologies
- **Language:** Python 3.12+ (Backend logic and Agent development).
- **Agent Framework:** Google Agent Development Kit (ADK) — Powers the interactive chat and agentic features.
- **Backend Framework:** FastAPI — High-performance web framework for the API layer.
- **Frontend Framework:** React — Building the user interface for the portfolio and chat interaction.

## Data & Storage
- **Primary Database:** Google Firestore — Serverless, NoSQL document database for managing portfolio content and agent session data.
- **Object Storage:** Google Cloud Storage (GCS) — Storing static assets and telemetry logs.

## Infrastructure & Deployment
- **Cloud Platform:** Google Cloud Platform (GCP).
- **Compute:** Google Cloud Run — Serverless execution for the backend and frontend.
- **IaC:** Terraform — Managing cloud infrastructure as code.
- **CI/CD:** Google Cloud Build — Automated build and deployment pipelines.

## Development & Quality Tools
- **Package Manager:** `uv` — Fast Python package and environment management.
- **Ingestion & CLI:** `typer`, `httpx`, `PyYAML` — Powering the hybrid resource ingestion system.
- **Linting & Formatting:** `ruff` — Extremely fast Python linter and code formatter.
- **Testing:** `pytest` — Feature-rich testing framework for unit and integration tests.
- **Quality Checks:** `codespell` — Checking for common misspellings in code and documentation.

## Observability
- **Telemetry:** OpenTelemetry — Instrumenting the application for traces and metrics.
- **Monitoring:** Google Cloud Trace — Visualizing application latency and agent performance.
- **Logging:** Google Cloud Logging — Centralised log management.
