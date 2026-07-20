# ==============================================================================
# Cloud Scheduler for Automated Ingestion
# ==============================================================================

# Defines the Cloud Scheduler job to trigger daily portfolio updates.
# Uses OIDC token authentication signed by a dedicated service account to
# securely call the FastAPI admin refresh endpoint.

# 1. Create a dedicated service account for Cloud Scheduler
resource "google_service_account" "scheduler" {
  account_id   = "${var.project_name}-scheduler"
  display_name = "Cloud Scheduler Service Account"
  project      = var.project_id
}

# 2. Create the Cloud Scheduler Job to run daily at midnight
resource "google_cloud_scheduler_job" "refresh_job" {
  name             = "${var.project_name}-refresh-job"
  description      = "Triggers daily portfolio ingestion at midnight (Europe/London)"
  schedule         = "0 0 * * *"
  time_zone        = "Europe/London"
  project          = var.project_id
  region           = var.region
  attempt_deadline = "300s"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.app.uri}/api/admin/refresh"

    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = google_service_account.scheduler.email
      audience              = "${google_cloud_run_v2_service.app.uri}/api/admin/refresh"
    }
  }

  depends_on = [
    google_project_service.deploy_project_services,
  ]
}
