# Gemini Guidance

We are building a dev portfolio application. The goal is to showcase my blogs, projects and public code repos. The application should use a Gemini agent to be able to answer relevant questions. 

## Portfolio Resources

- Blogs
  - On Medium: https://medium.com/@derailed.dash
  - On dev.to: https://dev.to/deraileddash
- My Advent of Code Walkthroughs and Python Learning site: https://aoc.just2good.co.uk/
- My public repos on GitHub: https://github.com/derailed-dash
- My LinkedIn: https://www.linkedin.com/in/darren-lester-architect/

## Key Docs

- @README.md - repo overview and dev guidance
- @GEMINI.md - guidance for you, the agent
- @conductor/product.md - an overview of this portfolio site as a "product"
- @conductor/tech-stack.md - an overview of the tech stack
- @TODO.md - list of tasks to complete
- @Makefile - dev commands
- @docs/design-and-walkthrough.md - design and walkthrough, including design decisions and implementation
- @docs/testing.md - testing docs, including descriptions of all tests
- @deployment/README.md - deployment docs

## Rules

- Check the GOOGLE_CLOUD_PROJECT is set to "dazbo-portfolio". If gcloud thinks it's anything else, you will have permission issues or incorrect resources deployed.
- ALWAYS use the adk-docs-mcp to answer questions about building agents with ADK. If you can't use this MCP, you MUST alert me rather than falling back to what you know.
- Key docs should be updated as you make changes.
- Always include top-of-file docstrings in every Python file you create or edit. This should include a description of what the file does, why it exists, and how it works.

## References 

- [Vector Search in Firestore](https://docs.cloud.google.com/firestore/native/docs/vector-search)
- [Text embeddings with Gemini Embeddings](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings)
- [Configure Secrets for Cloud Run Services](https://docs.cloud.google.com/run/docs/configuring/services/secrets)
 
### Firestore MCP

- [ADK with MCP - Bakery Application](https://github.com/google/mcp/blob/main/examples/launchmybakery/adk_agent/mcp_bakery_app/tools.py)
- [MCP in ADK](https://google.github.io/adk-docs/tools-custom/mcp-tools/)
- [Use Firestore Remote MCP](https://docs.cloud.google.com/firestore/native/docs/use-firestore-mcp)
- [firestore.googleapis.com reference](https://docs.cloud.google.com/firestore/docs/reference/mcp)
- [Firestore list_documents](https://docs.cloud.google.com/firestore/docs/reference/mcp/tools_list/list_documents)
- [Firestore get_document](https://docs.cloud.google.com/firestore/docs/reference/mcp/tools_list/get_document)
- [Firestore get_collections](https://docs.cloud.google.com/firestore/docs/reference/mcp/tools_list/list_collections)
- [Manage Firestore via Firestore MCP Server](https://medium.com/google-cloud/how-to-manage-your-firestore-database-with-natural-language-step-by-step-examples-bbc764f93d70)

## Firestore MCP + ADK Implementation Best Practices

### 1. Synchronous Definition
For production deployments (e.g., Cloud Run), the `Agent` and `McpToolset` **must be defined synchronously** in `agent.py`. Avoid asynchronous factory patterns for the root agent to ensure the container initializes correctly.

### 2. Connection Configuration
Use the `StreamableHTTPConnectionParams` class from `google.adk.tools.mcp_tool.mcp_session_manager` to connect to the remote Google-managed endpoint.
- **Endpoint URL:** `https://firestore.googleapis.com/mcp`
- **Important:** The Firestore MCP server requires a `POST` request to initiate the SSE session, which `StreamableHTTPConnectionParams` handles correctly. `SseConnectionParams` may fail with a `405 Method Not Allowed` because it defaults to a `GET` request.

### 3. Authentication
The Firestore MCP server requires valid Google Cloud authentication. You must provide an `Authorization` header with a valid access token in the connection parameters.
```python
credentials, _ = google.auth.default()
# Ensure token is fresh
credentials.refresh(google.auth.transport.requests.Request())

firestore_mcp = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://firestore.googleapis.com/mcp",
        headers={"Authorization": f"Bearer {credentials.token}"}
    ),
    # ...
)
```

### 4. Security & Tool Filtering
Always use the `tool_filter` parameter in `McpToolset` to adhere to the principle of least privilege. For a read-only portfolio assistant, restrict the agent to:
- `list_documents`
- `get_document`
- `list_collections`

### 5. Known Limitations & Bugs
- **`list_documents` & `get_document` Schema Bug:** The managed Firestore MCP server returns literal JSON `null` for fields its own schema defines as an enum (e.g. `nullValue: "NULL_VALUE"`). This causes the `mcp` Python SDK to crash.
  - **Workaround:** We use a **Monkey-Patch** in `app/agent.py` to disable the strict validation: `mcp.client.session.ClientSession._validate_tool_result = _skip_validation` (where `_skip_validation` is an `async` function that returns `None`).
  - **Strategy:** We still maintain a **Hybrid Tooling Approach** where `search_portfolio` (bespoke) handles broad discovery and counting, while the patched MCP `get_document` handles detailed retrieval.

### 6. Infrastructure Prerequisites
- **IAM Roles:** The Service Account requires `roles/mcp.toolUser` and `roles/datastore.user`.
- **API Enablement:** Both the Firestore API and the MCP server must be enabled:
  ```bash
  gcloud beta services mcp enable firestore.googleapis.com
  ```
- **Authentication:** Authentication is handled automatically via Google Application Default Credentials (ADC) when using `SseConnectionParams` in a GCP environment.

### 7. Dependency & Schema Mapping
- **Dynamic Discovery:** Do not manually define tool schemas for Firestore. The `McpToolset` performs dynamic discovery via the `tools/list` MCP method and maps them to ADK-compatible tool definitions on initialization.

