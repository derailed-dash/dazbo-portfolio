# Specification: Infrastructure Refinement & Firestore Provisioning

## Overview
This track focuses on ensuring the project's infrastructure, managed via Terraform, is correctly configured for the new architecture. This includes explicitly provisioning Google Firestore in Native Mode and removing legacy components like Cloud SQL and other unused resources to maintain a lean and cost-effective environment. Additionally, it involves documenting the deployment process comprehensively.

## Functional Requirements
- **Firestore Provisioning:** Update Terraform configurations to ensure Google Firestore is provisioned in **Native Mode**.
- **Legacy Cleanup:** Identify and remove Terraform resources and variables related to Cloud SQL.
- **Resource Audit:** Identify other unused infrastructure components (e.g., Service Accounts, APIs, Storage Buckets) and propose their removal before action.
- **Environment Parity:** Ensure both `dev` and production-level Terraform configurations are updated.
- **Documentation:** Populate `deployment/README.md` with a full walkthrough of the Terraform configuration, its purpose, and instructions on how to execute it.

## Non-Functional Requirements
- **Safety:** Verify and suggest resources for removal before deleting them.
- **Automation:** Use standard `terraform apply` for resource lifecycle management where possible.
- **Security:** Ensure Service Account roles are following the principle of least privilege after removal of legacy dependencies.

## Acceptance Criteria
- Firestore is successfully provisioned and accessible in Native Mode.
- No Cloud SQL resources exist in the Terraform state or configuration files.
- The project environment is cleaned of identified and approved redundant resources.
- `terraform plan` shows a clean state with no pending unexpected changes.
- `deployment/README.md` is populated with a comprehensive deployment guide.

## Out of Scope
- Migrating actual data from legacy systems (this track is infrastructure-only).
- Setting up complex Firestore Security Rules (beyond basic setup if needed).
