# ==============================================================================
# Storage & Database Resources
# ==============================================================================

# Manages stateful resources and artifact storage.
# 1. Cloud Storage: Buckets for application logs and telemetry.
# 2. Artifact Registry: Docker repository for storing application images.
# 3. Firestore: NoSQL database in Native mode for application data.

provider "google" {
  region                = var.region
  user_project_override = true
}

# We'll create the state bucket manually - a pre-req to using this Terraform configuration
# resource "google_storage_bucket" "tf_state_bucket" {
#   name                        = "${var.project_id}-tf-state"
#   location                    = var.region
#   project                     = var.project_id
#   uniform_bucket_level_access = true
#   force_destroy               = true

#   depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
# }

resource "google_storage_bucket" "assets_bucket" {
  name                        = "${var.project_id}-assets"
  location                    = var.region
  project                     = var.project_id
  uniform_bucket_level_access = true
  force_destroy               = true

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "OPTIONS"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  depends_on = [resource.google_project_service.deploy_project_services]
}

resource "google_storage_bucket_iam_member" "assets_bucket_public_access" {
  bucket = google_storage_bucket.assets_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_artifact_registry_repository" "repo-artifacts-genai" {
  location      = var.region
  repository_id = "${var.project_name}-repo"
  description   = "Repo for Generative AI applications"
  format        = "DOCKER"
  project       = var.cicd_runner_project_id
  depends_on    = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

resource "google_storage_bucket" "logs_data_bucket" {
  for_each                    = toset(local.all_project_ids)
  name                        = "${each.value}-logs"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

resource "google_firestore_database" "database" {
  project                           = var.project_id
  name                              = "(default)"
  location_id                       = var.region
  type                              = "FIRESTORE_NATIVE"
  delete_protection_state           = "DELETE_PROTECTION_DISABLED"
  point_in_time_recovery_enablement = "POINT_IN_TIME_RECOVERY_ENABLED"
  depends_on                        = [resource.google_project_service.deploy_project_services]
}