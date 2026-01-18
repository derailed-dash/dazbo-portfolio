# ====================================================================
# Dedicated Cloud Logging Bucket for GenAI Telemetry
# ====================================================================

# Create a custom Cloud Logging bucket for GenAI telemetry logs with long-term retention
resource "google_logging_project_bucket_config" "genai_telemetry_bucket" {
  project          = var.project_id
  location         = var.region
  bucket_id        = "${var.project_name}-genai-telemetry"
  retention_days   = 3650  # 10 years retention (maximum allowed)
  enable_analytics = false # Changed to false as linked datasets (BigQuery) are removed
  description      = "Dedicated Cloud Logging bucket for ${var.project_name} GenAI telemetry with 10 year retention"

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.deploy_project_services]
}

# Log sink to route only GenAI telemetry logs to the dedicated bucket
# Filter by bucket name in the GCS path (which includes project_name) to isolate this agent's logs
resource "google_logging_project_sink" "genai_logs_to_bucket" {
  name        = "${var.project_name}-genai-logs"
  project     = var.project_id
  destination = "logging.googleapis.com/projects/${var.project_id}/locations/${var.region}/buckets/${google_logging_project_bucket_config.genai_telemetry_bucket.bucket_id}"
  filter      = "log_name=\"projects/${var.project_id}/logs/gen_ai.client.inference.operation.details\" AND (labels.\"gen_ai.input.messages_ref\" =~ \".*${var.project_name}.*\" OR labels.\"gen_ai.output.messages_ref\" =~ \".*${var.project_name}.*\")"

  unique_writer_identity = true
  depends_on             = [google_logging_project_bucket_config.genai_telemetry_bucket]
}

# ====================================================================
# Feedback Logs to Cloud Logging Bucket
# ====================================================================

# Log sink for user feedback logs - routes to the same Cloud Logging bucket
resource "google_logging_project_sink" "feedback_logs_to_bucket" {
  name        = "${var.project_name}-feedback"
  project     = var.project_id
  destination = "logging.googleapis.com/projects/${var.project_id}/locations/${var.region}/buckets/${google_logging_project_bucket_config.genai_telemetry_bucket.bucket_id}"
  filter      = var.feedback_logs_filter

  unique_writer_identity = true
  depends_on             = [google_logging_project_bucket_config.genai_telemetry_bucket]
}