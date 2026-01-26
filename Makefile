# Assign env variables if they are not already set
GOOGLE_GENAI_USE_VERTEXAI = true
SERVICE_NAME ?= dazbo-portfolio
APP_NAME ?= dazbo_portfolio
AGENT_NAME ?= dazbo_portfolio_chat_agent
MODEL ?= gemini-2.5-flash
MIN_INSTANCES ?= 0
GOOGLE_CLOUD_REGION ?= europe-west1
GOOGLE_CLOUD_LOCATION ?= global
GOOGLE_CLOUD_PROJECT ?= $(shell gcloud config get-value project)

# Install dependencies using uv package manager and npm
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.8.13/install.sh | sh; source $$HOME/.local/bin/env; }
	uv sync
	cd frontend && npm install

# Launch local ADK Web UI
playground:
	@echo "==============================================================================="
	@echo "| 🚀 Starting your agent playground...                                        |"
	@echo "|                                                                             |"
	@echo "| 🔍 IMPORTANT: Select the 'app' folder to interact with your agent.          |"
	@echo "==============================================================================="
	uv run adk web . --port 8501 --reload_agents

# Launch local development server with hot-reload
local-backend:
	uv run uvicorn app.fast_api_app:app --host localhost --port 8000 --reload

# Run React UI
react-ui:
	cd frontend && npm run dev

# Build and deploy the agent to Cloud Run (Manual / Development)
# Builds directly from source; not from Google Artifact Registry
# Usage: make deploy-cloud-run [IAP=true]
deploy-cloud-run:
	gcloud run deploy $(SERVICE_NAME) \
		--source . \
		--project $(GOOGLE_CLOUD_PROJECT) \
		--region $(GOOGLE_CLOUD_REGION) \
		--service-account="$$SERVICE_SA_EMAIL" \
		--max-instances=1 \
		--min-instances=$(MIN_INSTANCES) \
		--cpu-boost \
		--allow-unauthenticated \
		--set-env-vars="COMMIT_SHA=$(shell git rev-parse HEAD),APP_NAME=$(APP_NAME),AGENT_NAME=$(AGENT_NAME),MODEL=$(MODEL),GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI),GOOGLE_CLOUD_LOCATION=$(GOOGLE_CLOUD_LOCATION),LOG_LEVEL=DEBUG" \
		--labels=dev-tutorial=devnewyear2026 \
		$(if $(IAP),--iap)

# Build the unified container image
docker-build:
	docker build -t dazbo-portfolio:latest .

# Run the unified container locally
docker-run:
	docker run --rm -p 8080:8080 \
		-e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		-e FIRESTORE_DATABASE_ID="(default)" \
		-e GEMINI_API_KEY="$${GEMINI_API_KEY}" \
		-e GOOGLE_GENAI_USE_VERTEXAI="$${GOOGLE_GENAI_USE_VERTEXAI}" \
		-e MODEL="$${MODEL}" \
		-e GOOGLE_APPLICATION_CREDENTIALS="/code/application_default_credentials.json" \
		--mount type=bind,source=$${HOME}/.config/gcloud/application_default_credentials.json,target=/code/application_default_credentials.json,readonly \
		dazbo-portfolio:latest

# Set up development environment resources using Terraform
tf-plan:
	(cd deployment/terraform && terraform init && terraform plan --var-file vars/env.tfvars)

tf-apply:
	(cd deployment/terraform && terraform init && terraform apply --var-file vars/env.tfvars --auto-approve)

# Run unit and integration tests
test:
	uv sync --dev
	uv run pytest tests/unit && uv run pytest tests/integration

# Run frontend UI tests
ui-test:
	cd frontend && npm test -- --run

# Run code quality checks (codespell, ruff, ty)
lint:
	uv sync --dev --extra lint
	uv run codespell
	uv run ruff check . --diff
	uv run ruff format . --check --diff
	uv run ty check .