import asyncio
import json
from datetime import timedelta

import google.auth
import google.auth.transport.requests
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_mcp_schema():
    credentials, _ = google.auth.default()
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)

    url = "https://firestore.googleapis.com/mcp"
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json",
    }

    print(f"Connecting to {url}...")
    async with streamablehttp_client(
        url=url,
        headers=headers,
        timeout=timedelta(seconds=30),
    ) as streams:
        read_stream, write_stream, *_ = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            for tool in tools.tools:
                if tool.name in ["get_document", "list_collections"]:
                    print(f"\nTool: {tool.name}")
                    print(f"Description: {tool.description}")
                    print(f"Input Schema: {json.dumps(tool.inputSchema, indent=2)}")


if __name__ == "__main__":
    asyncio.run(test_mcp_schema())
