# ==============================================================================
# Service Account Definitions
# ==============================================================================

# Creates the Service Accounts (SAs) required for the application and pipeline.
# 1. CICD Runner SA: Used by Cloud Build to execute pipelines.
# 2. App SA: The runtime identity for the Cloud Run application.

resource "google_service_account" "cicd_runner_sa" {
  account_id   = "${var.project_name}-cb"
  display_name = "CICD Runner SA"
  project      = var.cicd_runner_project_id
  depends_on   = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}
# Agent service account
resource "google_service_account" "app_sa" {
  account_id   = "${var.project_name}-app"
  display_name = "${var.project_name} Agent Service Account"
  project      = var.project_id
  depends_on   = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}


