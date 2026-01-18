# Deployment & Infrastructure

This directory contains the Terraform configuration for provisioning and managing the Google Cloud Platform (GCP) infrastructure for the Dazbo Portfolio application.

## Overview

The infrastructure is designed to be serverless, scalable, and secure, leveraging GCP's managed services. It follows a modular approach with separate configurations for development and multi-environment (Staging/Production) deployments.

### Key Components

- **Cloud Run:** Hosts the containerized FastAPI backend and agent.
- **Google Firestore:** Serverless NoSQL document database in **Native Mode** for portfolio content and session management.
- **Cloud Storage (GCS):** Used for storing static assets and telemetry logs.
- **Artifact Registry:** Stores Docker images for the application.
- **Cloud Build:** Manages the CI/CD pipeline for automated deployments.
- **Cloud Logging & Trace:** Provides observability and long-term telemetry storage.


## Project Structure

```text
deployment/terraform/
├── vars/
│   └── env.tfvars        # Environment-specific variable values
├── apis.tf               # Google Cloud API enablement
├── build_triggers.tf     # Cloud Build trigger definitions for CI/CD
├── github.tf             # GitHub repository and connection configuration
├── iam.tf                # IAM bindings and permissions
├── locals.tf             # Local variable definitions and helpers
├── providers.tf          # Terraform provider configuration
├── service.tf            # Cloud Run service definition
├── service_accounts.tf   # Service Account definitions
├── storage.tf            # GCS buckets, Artifact Registry, and Firestore
├── telemetry.tf          # Cloud Logging buckets and telemetry sinks
└── variables.tf          # Input variable definitions
```

### Variable Propagation

Configuration flows from Terraform through to the runtime environment:

1.  **Definition**: Variables (e.g., `model`, `service_name`) are defined in `variables.tf` and populated via `env.tfvars`.
2.  **Build Configuration**: Terraform injects these values into the **Cloud Build Trigger** via substitutions (see `build_triggers.tf`).
3.  **Deployment**: When the trigger fires, Cloud Build receives these substitutions and passes them to the `gcloud run deploy` command (see `.cloudbuild/deploy-to-prod.yaml`).
4.  **Runtime**: The variables are set as **Environment Variables** on the Cloud Run service, accessible to the application at runtime.

### Configuration Sources (Why duplication?)

You may notice similar variables in `env.tfvars` and your local `.env` file. They serve distinct purposes:

-   **`deployment/terraform/vars/env.tfvars` (Infrastructure & CI/CD)**:
    -   Used by Terraform to configure the **Cloud Build Trigger**.
    -   Values are baked into the pipeline definition.
    -   *Source of Truth for automated deployments.*

-   **`.env` (Local Development)**:
    -   Used by your local runtime (`uvicorn`, `docker run`).
    -   Not visible to Terraform or Cloud Build.
    -   *Source of Truth for local testing.*

-   **`Makefile` (Bridging the gap)**:
    -   The `deploy-cloud-run` target uses conditional assignment (`NAME ?= value`).
    -   It allows you to use your local `.env` values (via `source .env`) to perform manual deployments that match the production configuration.

## Prerequisites

1.  **GCP Projects:**
    -   **Single Project Architecture:** The configuration uses a single `project_id` for resources. You can deploy to different environments by using different `env.tfvars` files, but the logical definition is unified.
2.  **Tools:**
    -   [Terraform](https://www.terraform.io/downloads) (>= 1.0.0)
    -   [gcloud CLI](https://cloud.google.com/sdk/docs/install)
3.  **Authentication:**
    ```bash
    gcloud auth application-default login
    ```

## Deployment Instructions

The easiest way to manage the infrastructure is using the provided `Makefile` in the project root.

### Quick Start (Makefile)

```bash
# Plan changes for your project
make tf-plan

# Apply changes
make tf-apply
```

### Manual Terraform Usage

If you prefer to run Terraform directly:

```bash
cd deployment/terraform

# Initialize Terraform
terraform init

# Plan changes
terraform plan -var-file="vars/env.tfvars"

# Apply changes
terraform apply -var-file="vars/env.tfvars"
```

## Maintenance & Cleanup

### Removing Legacy Resources

The infrastructure has been migrated from PostgreSQL to Firestore. Legacy SQL resources have been removed from the Terraform configuration. If you are cleaning up a pre-migration environment, `terraform apply` will automatically identify and propose the destruction of these resources.

### Telemetry & Observability

Telemetry data (prompts, responses, and traces) is captured and routed to dedicated Cloud Logging buckets with 10-year retention. This data can be queried directly via Cloud Logging or exported for further analysis.

## Security

- **Least Privilege:** Service accounts are assigned only the roles necessary for their function (e.g., `roles/aiplatform.user`, `roles/logging.logWriter`).
- **Identity-Aware Proxy (IAP):** Can be optionally enabled for Cloud Run services (see `service.tf`).
- **Deletion Protection:** Firestore databases are configured with `delete_protection_state = "DELETE_PROTECTION_DISABLED"` for development ease, but should be enabled for critical production environments.
