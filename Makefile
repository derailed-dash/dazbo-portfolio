# Install dependencies using uv package manager
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.8.13/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync

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

# Deploy the agent remotely
# Usage: make deploy [IAP=true] [PORT=8080] - Set IAP=true to enable Identity-Aware Proxy, PORT to specify container port
deploy-cloud-run:
	PROJECT_ID=$$(gcloud config get-value project) && \
	gcloud beta run deploy dazbo-portfolio \
		--source . \
		--memory "4Gi" \
		--project $$PROJECT_ID \
		--region $$GOOGLE_CLOUD_LOCATION \
		--update-env-vars \
		"COMMIT_SHA=$(shell git rev-parse HEAD)" \
		$(if $(IAP),--iap) \
		$(if $(PORT),--port=$(PORT))

# Build the unified container image
docker-build:
	docker build -t dazbo-portfolio:latest .

# Run the unified container locally
docker-run:
	docker run --rm -p 8080:8080 \
		-e GOOGLE_CLOUD_PROJECT=$$(gcloud config get-value project) \
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

# Run code quality checks (codespell, ruff, ty)
lint:
	uv sync --dev --extra lint
	uv run codespell
	uv run ruff check . --diff
	uv run ruff format . --check --diff
	uv run ty check .