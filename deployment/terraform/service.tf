# ==============================================================================
# Cloud Run Service Definition
# ==============================================================================

# Defines the main application Cloud Run service.
# - Configures container image (initially "hello-world", replaced by CI/CD).
# - Sets resource limits (CPU, Memory) and scaling parameters.
# - Injects environment variables for runtime configuration (e.g., Log Bucket).
# - Ties the service to its dedicated Service Account.

resource "google_cloud_run_v2_service" "app" {
  name                = var.project_name
  location            = var.region
  project             = var.project_id
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"
  labels = {
    "created-by"                  = "adk"
  }

  template {
    containers {
      # Placeholder, will be replaced by the CI/CD pipeline
      image = "us-docker.pkg.dev/cloudrun/container/hello"
      resources {
        limits = {
          cpu    = "2"
          memory = "4Gi"
        }
        cpu_idle = false
      }

      env {
        name  = "LOGS_BUCKET_NAME"
        value = google_storage_bucket.logs_data_bucket[var.project_id].name
      }

      env {
        name = "DAZBO_SYSTEM_PROMPT"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.dazbo_system_prompt.secret_id
            version = "latest"
          }
        }
      }

      env {
        name  = "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"
        value = "NO_CONTENT"
      }
    }

    service_account                = google_service_account.app_sa.email
    max_instance_request_concurrency = 40

    scaling {
      max_instance_count = 1
    }

    session_affinity = true
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  # This lifecycle block prevents Terraform from overwriting fields managed by Cloud Build
  # (image, environment variables, client metadata) during deployments.
  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image,
      template[0].containers[0].env,
    ]
  }

  # Make dependencies conditional to avoid errors.
  depends_on = [
    google_project_service.deploy_project_services,
  ]
}

# Allow unauthenticated invocations for the public website
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_v2_service.app.location
  project  = google_cloud_run_v2_service.app.project
  service  = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
