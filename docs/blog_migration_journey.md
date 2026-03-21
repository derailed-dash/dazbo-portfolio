# The Great Migration: Trading My Bespoke Firestore Tools for a Managed MCP Server

*By Darren "Dazbo" Lester*

## Introduction: Why Settle for Bespoke?

If you've been following my journey building this portfolio, you'll know I’m a massive fan of the "Build Fast, Build Smart" philosophy. When I first sat down to wire up the Gemini agent that powers this site, I did the most "architect" thing possible: I built exactly what I needed from scratch.

I created a couple of Python-based tools — search_portfolio and get_content_details — to bridge the gap between my LLM and my Firestore data. They were reliable, they were well-tested, and frankly, they were "mine." But here’s the rub: as an Enterprise Cloud Architect, I’m always looking for the ROI. Why am I maintaining custom code for a standard database interaction when there’s a managed, protocol-based alternative available?

Enter the **Model Context Protocol (MCP)** and the managed Firestore MCP server. Today, I’m walking you through why — and how — I’m gutting those bespoke tools and replacing them with a standardised Google-managed service.

## The Secret Sauce: Tooling and Context

Before we dive into the "how," I want to highlight the tooling that’s making this migration possible. I’m not just "winging it" — I’m using the **Gemini CLI** with the **Conductor** extension to manage the entire implementation track. It keeps me on rails, ensuring I don't miss a single permission or test case.

To make sure my Gemini agent really "gets" the Google Agent Development Kit (ADK), I used a cheeky little command: `npx skills add google/adk-docs/skills`. This essentially gives the agent a brain transplant, equipping it with the latest best practices and API patterns directly from the source.

I've also been quite busy in my `GEMINI.md` file. I've populated it with a whole bunch of ADK + Firestore MCP references — think of it as a specialized knowledge base that the agent can tap into whenever it needs to verify a configuration detail.

> **Dazbo Pro-Tip:** I've been guiding my agent to build its context iteratively. Every time we hit a milestone — like finishing the infrastructure phase or finalizing this blog draft — I use the `/resume save` command in the Gemini CLI to create a checkpoint. If I mess something up in Phase 2, I can just rewind to a known-good state. It’s like having a "Quick Save" button for your IDE!

## The Starting Point: A Tale of Two Custom Tools

Let’s look at what we’re moving away from. My original setup was purely code-first. I had two main tools that I'd registered with my ADK agent:

1.  **`search_portfolio`**: This was my "broad brush" tool. It would hit Firestore, pull back projects and blogs, and do some in-memory filtering (yeah, I know, I was going to optimise that later!) to find matches for the user's query.
2.  **`get_content_details`**: This was the "surgical" tool. Give it an ID, and it would fetch the full Markdown body or metadata for a specific item.

In `app/agent.py`, it looked like this:

```python
from app.tools.content_details import get_content_details
from app.tools.portfolio_search import search_portfolio

# ... later in the agent config ...
tools=[search_portfolio, get_content_details],
```

It worked like a charm. But it meant my agent was tightly coupled to my specific Python implementation. If I wanted to use a different agent framework or a different LLM host tomorrow, I’d have to port all that tool logic. That’s not very "Enterprise," is it?

## Why the Move to MCP?

The **Model Context Protocol (MCP)** is a game-changer because it standardises the "handshake" between an LLM and external data. By moving to the managed Firestore MCP server at `firestore.googleapis.com/mcp`, I’m shifting the burden of tool maintenance back to Google.

### The Architectural Rationale:
- **Reduced Code Surface**: I can delete two entire Python files and a bunch of service-layer logic. Less code means fewer bugs and less technical debt.
- **Protocol-First Integration**: My agent now speaks a standard language (MCP) to talk to Firestore. This makes the architecture far more portable.
- **Managed Intelligence**: The managed MCP server provides tools like `list_documents` and `get_document` that are already optimised for Firestore’s native capabilities.

## Phase 1: Infrastructure and Permissions (The Boring but Critical Bit)

Before I could even think about touching the Python code, I had to ensure the GCP plumbing was right. This is where most developers trip up — don't neglect your IAM!

I updated my Terraform configuration to enable `firestore.googleapis.com` and, more importantly, I had to assign the right roles to my application's Service Account:
- `roles/mcp.toolUser`: This is the key that lets the agent actually "talk" to the MCP server.
- `roles/datastore.user`: Standard permissions to read the data.

I also had to explicitly enable the MCP server for my project using the `gcloud` CLI:
```bash
gcloud beta services mcp enable firestore.googleapis.com
```

> **Dazbo Pro-Tip:** If you're running this in a CI/CD pipeline (like my Google Cloud Build setup), make sure these permissions are baked into your service account *before* you try to deploy the new agent code. There's nothing worse than a "Permission Denied" error in the middle of a deployment!

## Phase 2: Agent Integration (The Fun Part)

This is where the magic happens. Instead of manual imports, I’m using the ADK’s `McpToolset`. This class is brilliant — it handles the connection to the remote MCP server and automatically "discovers" the tools it offers.

Here’s the plan for the new `app/agent.py` logic:

```python
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams

# ...

firestore_mcp = McpToolset(
    connection_params=SseConnectionParams(
        url="https://firestore.googleapis.com/mcp"
    ),
    tool_filter=['list_documents', 'get_document', 'list_collections']
)

root_agent = PortfolioAgent(
    # ...
    tools=[firestore_mcp],
)
```

### The "About Me" Gotcha
One thing my custom tools handled nicely was a shortcut for the "About Me" page. With the new generic MCP tools, I need to be more explicit in my agent's instructions. I’ve updated the system prompt to tell the agent: *"If they want to know about Dazbo, use `get_document` to fetch the 'about' document from the 'content' collection."*

## What’s Next?

I’m currently in the middle of Phase 2 — wiring this all up and writing the integration tests to prove it works. Once that's done, I'll be deleting those old custom tools with a very satisfied click of the 'Delete' key.

### Why this way and not another?
I *could* have stuck with my custom tools and just refactored them to be cleaner. But that’s a local optimisation. By adopting MCP, I’m future-proofing the portfolio. If Google releases a new Firestore tool tomorrow, my agent gets it automatically without me writing a single line of Python. That’s the kind of architectural ROI I live for.

## Wrapping Up (For Now)

This migration isn't just about changing a few lines of code; it's a shift in how we think about agentic capabilities. We're moving from "I'll build a tool for that" to "I'll connect to a service for that."

I'll be back with another update once Phase 3 (Cleanup) and Phase 4 (Final Verification) are complete. Until then, keep it pragmatic!

---
*Darren "Dazbo" Lester is an Enterprise Cloud Architect and a self-confessed Google AI enthusiast. He's probably drinking tea and looking at car parts right now.*
