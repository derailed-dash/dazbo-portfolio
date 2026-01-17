# ==============================================================================
# Local Variables & Helper Definitions
# ==============================================================================

# Defines local variables used for iteration and configuration consolidation.
# - Lists APIs to enable for different project types.
# - Maps environment names (prod, staging) to project IDs.
# - Aggregates project IDs for resource-wide operations.

locals {
  cicd_services = [
    "cloudbuild.googleapis.com",
    "aiplatform.googleapis.com",
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudtrace.googleapis.com",
  ]

  deploy_project_services = [
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "serviceusage.googleapis.com",
    "logging.googleapis.com",
    "cloudtrace.googleapis.com",
    "firestore.googleapis.com",
  ]

  deploy_project_ids = {
    prod    = var.prod_project_id
    staging = var.staging_project_id
  }

  all_project_ids = [
    var.cicd_runner_project_id,
    var.prod_project_id,
    var.staging_project_id
  ]

}

