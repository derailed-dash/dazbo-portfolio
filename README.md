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
├── scripts/                   # Convenience scripts, e.g. for environment setup
├── tests/                     # Unit, integration, and load tests
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── .env.template              # .env template file
├── .envrc                     # Optional auto env configuration file
├── GEMINI.md                  # Guidance for Gemini
├── Makefile                   # Development commands
├── pyproject.toml             # Project Python dependencies and configuration
├── README.md                  # This file
└── TODO.md                    # TODO list
```

## Developing With This Repo

### One-Time Setup

1. Create a Google Cloud project and attach a billing account.
2. Enable the required APIs.

    ```bash
    gcloud services enable --project=$GOOGLE_CLOUD_PROJECT \
      artifactregistry.googleapis.com \
      cloudbuild.googleapis.com \
      secretmanager.googleapis.com \
      run.googleapis.com \
      logging.googleapis.com \
      aiplatform.googleapis.com \
      serviceusage.googleapis.com \
      storage.googleapis.com \
      cloudtrace.googleapis.com \
      geminicloudassist.googleapis.com \
      firestore.googleapis.com
    ```

3. Create your API key, e.g. at https://aistudio.google.com/api-keys

4. Set up Firestore.

    ```bash
    # If NOT using Terraform
    gcloud firestore databases create --location=europe-west1 --type=firestore-native
    ```

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

| Command                 | Description                                                   |
| ----------------------- | ------------------------------------------------------------- |
| `make install`          | Install dependencies using uv                                 |
| `make playground`       | Launch local development environment using ADK Web UI         |
| `make lint`             | Run code quality checks                                       |
| `make test`             | Run unit and integration tests                                |
| `make deploy-cloud-run` | Deploy agent to Cloud Run                                     |
| `make local-backend`    | Launch local development server with hot-reload               |
| `make tf-plan`          | Plan Terraform deployment                                     |
| `make tf-apply`         | Deploy environment resources using Terraform                  |

For full command options and usage, refer to the [Makefile](Makefile).

## Deployment

### Dev Environment

You can test deployment towards a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make deploy-cloud-run
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

See [docs/design-and-walkthrough.md](docs/design-and-walkthrough.md) for a detailed design and walkthrough of the application.

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
