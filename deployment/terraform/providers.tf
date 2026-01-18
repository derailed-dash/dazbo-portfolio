# ==============================================================================
# Terraform Provider Configuration
# ==============================================================================

# Configures the required Terraform providers (Google, GitHub, Random).
# Sets up provider aliases for billing overrides and specific project contexts.

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.13.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7.0"
    }
  }
}

provider "google" {
  alias                 = "staging_billing_override"
  billing_project       = var.project_id
  region                = var.region
  user_project_override = true
}

provider "google" {
  alias                 = "prod_billing_override"
  billing_project       = var.project_id
  region                = var.region
  user_project_override = true
}
