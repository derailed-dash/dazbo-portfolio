# ==============================================================================
# Google Cloud API Enablement
# ==============================================================================

# Enables necessary Google Cloud APIs for the CI/CD, Staging, and Production projects.
# This ensures that all required services (e.g., Cloud Build, Cloud Run, Firestore) 
# are available before resources are provisioned.

resource "google_project_service" "cicd_services" {
  count              = length(local.cicd_services)
  project            = var.cicd_runner_project_id
  service            = local.cicd_services[count.index]
  disable_on_destroy = false
}

resource "google_project_service" "deploy_project_services" {
  for_each           = toset(local.deploy_project_services)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# Enable Cloud Resource Manager API for the CICD runner project
resource "google_project_service" "cicd_cloud_resource_manager_api" {
  project            = var.cicd_runner_project_id
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}
