# ==============================================================================
# Identity and Access Management (IAM) Configuration
# ==============================================================================

# Manages IAM roles and permissions for Service Accounts across projects.
#
# Key Responsibilities:
# - Grants CI/CD and deployment roles to the Cloud Build Service Account.
# - Assigns runtime permissions to the Application Service Account (e.g., Vertex AI, Logging).
# - Configures cross-project permissions for artifact access.

# Data source to get project numbers
# Data source to get project number
data "google_project" "project" {
  project_id = var.project_id
}

# 1. Assign roles for the CICD project
resource "google_project_iam_member" "cicd_project_roles" {
  for_each = toset(var.cicd_roles)

  project    = var.cicd_runner_project_id
  role       = each.value
  member     = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]

}

# 2. Assign roles for the other two projects (prod and staging)
# 2. Assign roles for the deployment project (Prod/Staging/Single)
resource "google_project_iam_member" "deployment_project_roles" {
  for_each = toset(var.cicd_sa_deployment_required_roles)

  project    = var.project_id
  role       = each.value
  member     = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}
# 3. Grant application SA the required permissions to run the application
# 3. Grant application SA the required permissions to run the application
resource "google_project_iam_member" "app_sa_roles" {
  for_each = toset(var.app_sa_roles)

  project    = var.project_id
  role       = each.value
  member     = "serviceAccount:${google_service_account.app_sa.email}"
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}


# 4. Allow Cloud Run service SA to pull containers stored in the CICD project
# 4. Allow Cloud Run service SA to pull containers stored in the CICD project
resource "google_project_iam_member" "cicd_run_invoker_artifact_registry_reader" {
  project = var.cicd_runner_project_id

  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:service-${data.google_project.project.number}@serverless-robot-prod.iam.gserviceaccount.com"
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}




# Special assignment: Allow the CICD SA to create tokens
resource "google_service_account_iam_member" "cicd_run_invoker_token_creator" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}
# Special assignment: Allow the CICD SA to impersonate himself for trigger creation
resource "google_service_account_iam_member" "cicd_run_invoker_account_user" {
  service_account_id = google_service_account.cicd_runner_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${resource.google_service_account.cicd_runner_sa.email}"
  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}
