# Terraform backend configuration
#
# Expects the bucket has already been created, e.g.
# gcloud storage buckets create -p $GOOGLE_CLOUD_PROJECT gs://${GOOGLE_CLOUD_PROJECT}-tf-state
#
# To migrate from local state to this GCS backend state, simply re-run terraform init
# and answer 'yes' to the prompt to copy the existing state to the new backend.

terraform {
  backend "gcs" {
    bucket = "dazbo-portfolio-tf-state" # variables not supported here
    prefix = "terraform/state"
  }
}