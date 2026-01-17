# ==============================================================================
# GitHub Repository & Connection Configuration
# ==============================================================================
#
# Manages the integration between Google Cloud and GitHub.
#
# Key Logic:
# 1. Existing Secrets: This configuration EXPECTS the GitHub PAT secret to already exist 
#    in Secret Manager (defined by `var.github_pat_secret_id`). It effectively imports/reads
#    this secret to authorize Cloud Build.
#
# 2. Connection Management (`var.connection_already_exists`):
#    - If false (default): Terraform attempts to CREATE a new Cloud Build Connection.
#      NOTE: If a connection with `var.host_connection_name` already exists manually, this will FAIL.
#    - If true: Terraform assumes the connection exists and simply references it directly.
#      Use this setting if you have already set up the connection via the Cloud Console.
#
# 3. Repository Linking:
#    - Connects the specified GitHub repository to the Cloud Build Connection, enabling triggers.

provider "github" {
  owner = var.repository_owner
}

# Try to get existing repo
data "github_repository" "existing_repo" {
  count = var.create_repository ? 0 : 1
  full_name = "${var.repository_owner}/${var.repository_name}"
}

# Only create GitHub repo if create_repository is true
resource "github_repository" "repo" {
  count       = var.create_repository ? 1 : 0
  name        = var.repository_name
  description = "Repository created with goo.gle/agent-starter-pack"
  visibility  = "private"

  has_issues      = true
  has_wiki        = false
  has_projects    = false
  has_downloads   = false

  allow_merge_commit = true
  allow_squash_merge = true
  allow_rebase_merge = true
  
  auto_init = false
}

# Reference existing GitHub PAT secret created by gcloud CLI
data "google_secret_manager_secret" "github_pat" {
  project   = var.cicd_runner_project_id
  secret_id = var.github_pat_secret_id
}

# Get CICD project data for Cloud Build service account
data "google_project" "cicd_project" {
  project_id = var.cicd_runner_project_id
}

# Grant Cloud Build service account access to GitHub PAT secret
resource "google_secret_manager_secret_iam_member" "cloudbuild_secret_accessor" {
  project   = var.cicd_runner_project_id
  secret_id = data.google_secret_manager_secret.github_pat.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:service-${data.google_project.cicd_project.number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
  depends_on = [resource.google_project_service.cicd_services]
}

# Create the GitHub connection (fallback for manual Terraform usage)
resource "google_cloudbuildv2_connection" "github_connection" {
  count      = var.connection_already_exists ? 0 : 1
  project    = var.cicd_runner_project_id
  location   = var.region
  name       = var.host_connection_name

  github_config {
    app_installation_id = var.github_app_installation_id
    authorizer_credential {
      oauth_token_secret_version = "${data.google_secret_manager_secret.github_pat.id}/versions/latest"
    }
  }
  depends_on = [
    resource.google_project_service.cicd_services,
    resource.google_project_service.deploy_project_services,
    resource.google_secret_manager_secret_iam_member.cloudbuild_secret_accessor
  ]
}

resource "google_cloudbuildv2_repository" "repo" {
  project  = var.cicd_runner_project_id
  location = var.region
  name     = var.repository_name
  
  # Use existing connection ID when it exists, otherwise use the created connection
  parent_connection = var.connection_already_exists ? "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}" : google_cloudbuildv2_connection.github_connection[0].id
  remote_uri       = "https://github.com/${var.repository_owner}/${var.repository_name}.git"
  depends_on = [
    resource.google_project_service.cicd_services,
    resource.google_project_service.deploy_project_services,
    data.github_repository.existing_repo,
    github_repository.repo,
    google_cloudbuildv2_connection.github_connection,
  ]
}
