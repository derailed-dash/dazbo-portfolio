# ==============================================================================
# Input Variable Definitions
# ==============================================================================

# Defines all input variables required for the Terraform configuration.
# Includes project IDs, region settings, repository details, and IAM roles.
# Values for these variables should be provided via a `terraform.tfvars` file or command-line arguments.

variable "project_name" {
  type        = string
  description = "Project name used as a base for resource naming"
  default     = "dazbo-portfolio"
}

variable "project_id" {
  type        = string
  description = "Google Cloud Project ID for resource deployment."
}

variable "cicd_runner_project_id" {
  type        = string
  description = "Google Cloud Project ID where CI/CD pipelines will execute."
}

variable "region" {
  type        = string
  description = "Google Cloud region for resource deployment."
  default     = "europe-west1"
}

variable "location" {
  type        = string
  description = "Google Cloud location used by Gemini model."
  default     = "global"
}

variable "host_connection_name" {
  description = "Name of the host connection to create in Cloud Build"
  type        = string
  default     = "dazbo-portfolio-github-connection"
}

variable "repository_name" {
  description = "Name of the repository you'd like to connect to Cloud Build"
  type        = string
}

variable "app_sa_roles" {
  description = "List of roles to assign to the application service account"
  type        = list(string)
  default = [

    "roles/aiplatform.user",
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
    "roles/storage.objectAdmin",
    "roles/serviceusage.serviceUsageConsumer",
    "roles/secretmanager.secretAccessor",
    "roles/datastore.user",
  ]
}

variable "cicd_roles" {
  description = "List of roles to assign to the CICD runner service account in the CICD project"
  type        = list(string)
  default = [
    "roles/run.invoker",
    "roles/storage.admin",
    "roles/aiplatform.user",
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
    "roles/artifactregistry.writer",
    "roles/cloudbuild.builds.builder"
  ]
}

variable "cicd_sa_deployment_required_roles" {
  description = "List of roles to assign to the CICD runner service account for the Staging and Prod projects."
  type        = list(string)
  default = [
    "roles/run.developer",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/aiplatform.user",
    "roles/storage.admin"
  ]
}

variable "repository_owner" {
  description = "Owner of the Git repository - username or organization"
  type        = string
}

variable "github_app_installation_id" {
  description = "GitHub App Installation ID for Cloud Build"
  type        = string
  default     = null
}

variable "github_pat_secret_id" {
  description = "GitHub PAT Secret ID created by gcloud CLI"
  type        = string
  default     = null
}

variable "connection_already_exists" {
  description = "Flag indicating if a Cloud Build connection already exists. if false, Terraform will attempt to create it."
  type        = bool
  default     = false
}

variable "create_repository" {
  description = "Flag indicating whether to create a new Git repository"
  type        = bool
  default     = false
}

variable "feedback_logs_filter" {
  type        = string
  description = "Log Sink filter for capturing feedback data. Captures logs where the `log_type` field is `feedback`."
  default     = "jsonPayload.log_type=\"feedback\" jsonPayload.service_name=\"dazbo-portfolio\""
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "dazbo-portfolio"
}

variable "app_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "dazbo_portfolio"
}

variable "agent_name" {
  description = "Name of the agent"
  type        = string
  default     = "dazbo-portfolio"
}

variable "google_genai_use_vertexai" {
  description = "Whether to use Vertex AI for Gemini"
  type        = string
  default     = "true"
}

variable "model" {
  description = "Gemini model to use"
  type        = string
  default     = "gemini-2.5-flash"
}

variable "app_domain_name" {
  description = "A list of domain names to be mapped to the service"
  type        = list(string)
}