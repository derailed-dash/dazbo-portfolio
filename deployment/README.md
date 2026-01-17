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
├── dev/                  # Isolated environment for local/individual development
│   ├── apis.tf           # Services to enable in the dev project
│   ├── iam.tf            # Service accounts and IAM roles for dev
│   ├── storage.tf        # GCS buckets and Firestore for dev
│   └── service.tf        # Cloud Run service definition for dev
├── modules/              # (Planned) Shared modules for common resources
├── apis.tf               # Global APIs for Staging/Prod/CICD projects
├── iam.tf                # Global IAM configuration
├── storage.tf            # Global GCS, Artifact Registry, and Firestore
├── service.tf            # Multi-environment Cloud Run definitions
└── telemetry.tf          # Cloud Logging buckets and sinks for telemetry
```

## Prerequisites

1.  **GCP Projects:**
    -   **Multi-Environment (Enterprise Approach):** Separate projects for Dev, Staging, and Prod.
    -   **Single Project (Simple Approach):** A single GCP project can be used with the `dev` configuration for all purposes.
2.  **Tools:**
    -   [Terraform](https://www.terraform.io/downloads) (>= 1.0.0)
    -   [gcloud CLI](https://cloud.google.com/sdk/docs/install)
3.  **Authentication:**
    ```bash
    gcloud auth application-default login
    ```

## Deployment Instructions

### 1. Single Project or Development Environment (`dev`)

The `dev` environment is intended for quick iterations, isolated testing, or **single-project deployments**. It is the simplest way to get the infrastructure running.

```bash
cd deployment/terraform/dev

# Initialize Terraform
terraform init

# Plan changes
# Use your project ID as the 'dev_project_id'
terraform plan -var-file="vars/env.tfvars" -var="dev_project_id=YOUR_PROJECT_ID"

# Apply changes
terraform apply -var-file="vars/env.tfvars" -var="dev_project_id=YOUR_PROJECT_ID"
```

### 2. Multi-Environment (Staging & Production)

The root Terraform configuration manages the full pipeline, including CI/CD triggers and environment parity.

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
