# Issue Report: Firestore MCP Schema Mismatch (Null vs. Enum)

## Summary
The managed Firestore MCP server (`https://firestore.googleapis.com/mcp`) returns literal JSON `null` values for optional fields that its own JSON schema defines as an enum (specifically, the `nullValue: "NULL_VALUE"` pattern). This causes strict client-side validation libraries (such as the `mcp` Python SDK and Pydantic) to crash, as they expect the string `"NULL_VALUE"` but receive `null`.

## Environment
- **Endpoint**: `https://firestore.googleapis.com/mcp`
- **Method**: SSE (Streamable HTTP POST)
- **Tools Affected**: `list_documents`, `get_document`
- **Client SDK**: `mcp` Python SDK (strict jsonschema validation)

## Reproduction Steps
1. Create a Firestore document with an optional field left unset (e.g., a field that would normally contain a string or reference).
2. Use the Firestore MCP `get_document` or `list_documents` tool to retrieve this document.
3. Observe the raw JSON response.

### Diagnostic Script
A standalone reproduction script is available at `scripts/test_mcp_bug.py`. This script connects to the MCP endpoint and inspects the raw tool output.

### Observed Behavior
The server returns:
```json
{
  "fields": {
    "some_optional_field": null
  }
}
```

### Expected Behavior (According to Schema)
The tool's input schema for these fields defines them as an object that must contain exactly one key. For a null value, it should be:
```json
{
  "fields": {
    "some_optional_field": {
      "nullValue": "NULL_VALUE"
    }
  }
}
```

## Impact
Strict Model Context Protocol (MCP) clients perform validation against the tool's reported `inputSchema`. When the server sends a response that violates this schema (sending `null` instead of the expected enum structure), the client-side validation fails, resulting in a `RuntimeError` or session termination.

## Workaround (Monkey-Patch)
To allow the application to function, we implemented a monkey-patch in the `mcp` Python SDK to bypass the result validation:

```python
import mcp.client.session

async def _skip_validation(self, name, result):
    # Bypass strict schema validation to handle server-side nulls
    return None

mcp.client.session.ClientSession._validate_tool_result = _skip_validation
```

## Recommendation
Update the Firestore MCP server implementation to ensure that unset fields are either omitted from the response or correctly formatted as the defined `"NULL_VALUE"` enum string, adhering to the tool's published JSON schema.
