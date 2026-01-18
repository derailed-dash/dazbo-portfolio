# ==============================================================================
# Secret Manager Definitions
# 
# Create secrets in Secret Manager.
# Does NOT create any values
# ==============================================================================

resource "google_secret_manager_secret" "dazbo_system_prompt" {
  project   = var.project_id
  secret_id = "dazbo-system-prompt"

  replication {
    auto {}
  }
}