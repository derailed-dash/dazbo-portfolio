# Project name used for resource naming
project_name = "dazbo-portfolio"

# Your Google Cloud Project ID for resource deployment
project_id = "dazbo-portfolio"

# Your Google Cloud project ID that will be used to host the Cloud Build pipelines.
cicd_runner_project_id = "dazbo-portfolio"

# Name of the host connection you created in Cloud Build
connection_already_exists = true # Do not try to create a new connection
host_connection_name = "dazbo-portfolio-gh-conn"
github_pat_secret_id = "dazbo-portfolio-gh-conn-github-oauthtoken-5a4dea"

repository_owner = "derailed-dash"

# Name of the repository you added to Cloud Build
repository_name = "dazbo-portfolio"

# The Google Cloud region you will use to deploy the infrastructure
region = "europe-west1"

# Service Configuration
service_name = "dazbo_portfolio"
agent_name = "dazbo_portfolio_chat_agent"
google_genai_use_vertexai = "true"
model = "gemini-3-flash-preview"
location = "global"
