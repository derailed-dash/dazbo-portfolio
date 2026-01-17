# dazbo-portfolio

A development portfolio application, with React frontend, and an ADK/Gemini-based chat interface. The goal of the portfolio application is to showcase my blogs, projects and public code repos.

## Repo Metadata

Author: Darren "Dazbo" Lester

## Project Structure

```
dazbo-portfolio/
├── app/                       # Core agent code
│   ├── agent.py               # Main agent logic
│   ├── fast_api_app.py        # FastAPI Backend server
│   └── app_utils/             # App utilities and helpers
├── .cloudbuild/               # CI/CD pipeline configurations for Google Cloud Build
├── deployment/                # Infrastructure and deployment scripts
│   └── terraform/             # Terraform configuration
├── notebooks/                 # Jupyter notebooks for prototyping and evaluation
├── tests/                     # Unit, integration, and load tests
├── .env.template              # .env template file
├── .envrc                     # Optional auto env configuration file
├── GEMINI.md                  # Guidance for Gemini
├── Makefile                   # Development commands
├── pyproject.toml             # Project Python dependencies and configuration
└── README.md                  # This file
```

## Developing With This Repo

### Per Dev Session (Once One-Time Setup Tasks Have Been Completed)

**DO THIS STEP BEFORE EACH DEV SESSION**

To configure your shell for a development session, **source** the `scripts/setup-env.sh` script. This will handle authentication, set the correct Google Cloud project, install dependencies, and activate the Python virtual environment.

```bash
source scripts/setup-env.sh [--noauth]
```

### Using Direnv

Note that you can automate loading the `setup-env.sh` script by installing [direnv](https://direnv.net/), and then including the `.envrc` in the project folder. E.g.

```bash
sudo apt install direnv

# Add eval "$(direnv hook bash)" to your .bashrc
echo "eval \"\$(direnv hook bash)\"" >> ~/.bashrc

# Then, from this project folder:
direnv allow
```

## Useful Commands

| Command              | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| `make install`       | Install dependencies using uv                                           |
| `make playground`    | Launch local development environment using ADK Web UI                   |
| `make lint`          | Run code quality checks                                                 |
| `make test`          | Run unit and integration tests                                          |
| `make deploy`        | Deploy agent to Cloud Run                                               |
| `make local-backend` | Launch local development server with hot-reload                         |
| `make setup-dev-env` | Set up development environment resources using Terraform                |

For full command options and usage, refer to the [Makefile](Makefile).

## Deployment

> **Note:** For a streamlined one-command deployment of the entire CI/CD pipeline and infrastructure using Terraform, you can use the [`agent-starter-pack setup-cicd` CLI command](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html). Currently supports GitHub with both Google Cloud Build and GitHub Actions as CI/CD runners.

### Dev Environment

You can test deployment towards a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make deploy
```

The repository includes a Terraform configuration for the setup of the Dev Google Cloud project.
See [deployment/README.md](deployment/README.md) for instructions.

### Running in a Local Container

```bash
# from project root directory

# Get a unique version to tag our image
export VERSION=$(git rev-parse --short HEAD)

# To build as a container image
docker build -t $SERVICE_NAME:$VERSION .

# To run as a local container
# We need to pass environment variables to the container
# and the Google Application Default Credentials (ADC)
docker run --rm -p 8080:8080 \
  -e GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT -e GOOGLE_CLOUD_REGION=$GOOGLE_CLOUD_REGION \
  -e LOG_LEVEL=$LOG_LEVEL \
  -e APP_NAME=$APP_NAME \
  -e AGENT_NAME=$AGENT_NAME \
  -e GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI \
  -e MODEL=$MODEL \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/.config/gcloud/application_default_credentials.json" \
  --mount type=bind,source=${HOME}/.config/gcloud,target=/app/.config/gcloud \
   $SERVICE_NAME:$VERSION
```

### Production Deployment

The repository includes a Terraform configuration for the setup of a production Google Cloud project. Refer to [deployment/README.md](deployment/README.md) for detailed instructions on how to deploy the infrastructure and application.

## Design

### Design decisions:

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

## Monitoring and Observability

The application provides two levels of observability:

**1. Agent Telemetry Events (Always Enabled)**
- OpenTelemetry traces and spans exported to **Cloud Trace**
- Tracks agent execution, latency, and system metrics

**2. Prompt-Response Logging (Configurable)**
- GenAI instrumentation captures LLM interactions (tokens, model, timing)
- Exported to **Google Cloud Storage** (JSONL), **BigQuery** (external tables), and **Cloud Logging** (dedicated bucket)

| Environment | Prompt-Response Logging |
|-------------|-------------------------|
| **Local Development** (`make playground`) | ❌ Disabled by default |
| **Deployed Environments** (via Terraform) | ✅ **Enabled by default** (privacy-preserving: metadata only, no prompts/responses) |

**To enable locally:** Set `LOGS_BUCKET_NAME` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`.

**To disable in deployments:** Edit Terraform config to set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false`.

See the [observability guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/observability.html) for detailed instructions, example queries, and visualization options.
