# ==============================================================================
# Cloud Build Triggers for CI/CD
# ==============================================================================

# Defines Cloud Build triggers to automate the software delivery pipeline.
#
# Triggers include:
# 1. PR Checks: Runs tests and linting on pull requests to the main branch.
# 2. CD Pipeline: Deploys to the Staging environment on pushes to main.
# 3. Prod Deployment: Manual approval trigger to promote builds to Production.

# a. Create PR checks trigger
resource "google_cloudbuild_trigger" "pr_checks" {
  name            = "pr-${var.project_name}"
  project         = var.cicd_runner_project_id
  location        = var.region
  description     = "Trigger for PR checks"
  service_account = resource.google_service_account.cicd_runner_sa.id

  repository_event_config {
    repository = "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}/repositories/${var.repository_name}"
    pull_request {
      branch = "main"
    }
  }

  filename = ".cloudbuild/pr_checks.yaml"
  included_files = [
    "app/**",
    "data_ingestion/**",
    "deployment/**",
    "frontend/**",
    "tests/**",
    "uv.lock"
  ]
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
  depends_on = [
    resource.google_project_service.cicd_services, 
    resource.google_project_service.deploy_project_services, 
    google_cloudbuildv2_connection.github_connection, 
    google_cloudbuildv2_repository.repo
  ]
}

# b. Create Deploy to production trigger
resource "google_cloudbuild_trigger" "deploy_to_prod_pipeline" {
  name            = "deploy-${var.project_name}"
  project         = var.cicd_runner_project_id
  location        = var.region
  description     = "Trigger for deployment to production"
  service_account = resource.google_service_account.cicd_runner_sa.id
  repository_event_config {
    repository = "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}/repositories/${var.repository_name}"
    push {
      branch = "main"
    }
  }
  filename = ".cloudbuild/deploy-to-prod.yaml"
  included_files = [
    "app/**",
    "data_ingestion/**",
    "deployment/**",
    "frontend/**",
    "tests/**",
    "uv.lock"
  ]
  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
  approval_config {
    approval_required = true
  }
  substitutions = {
    _LOGS_BUCKET_NAME_PROD       = resource.google_storage_bucket.logs_data_bucket[var.project_id].name
    _APP_SERVICE_ACCOUNT         = google_service_account.app_sa.email
    _REGION                      = var.region
    _LOCATION                    = var.location
    _ARTIFACT_REGISTRY_REPO_NAME = resource.google_artifact_registry_repository.repo-artifacts-genai.repository_id
    _SERVICE_NAME                = var.service_name
    _AGENT_NAME                  = var.agent_name
    _GOOGLE_GENAI_USE_VERTEXAI   = var.google_genai_use_vertexai
    _MODEL                       = var.model
    _MAX_INSTANCES               = "1"
    _LOG_LEVEL                   = "DEBUG"
  }

  depends_on = [
    resource.google_project_service.cicd_services, 
    resource.google_project_service.deploy_project_services, 
    google_cloudbuildv2_connection.github_connection, 
    google_cloudbuildv2_repository.repo
  ]

}
