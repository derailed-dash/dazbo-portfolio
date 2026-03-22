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

## Phase 1: Infrastructure and Permissions (The Boring but Critical Bit)

Before I could even think about touching the Python code, I had to ensure the GCP plumbing was right. This is where most developers trip up — don't neglect your IAM!

I updated my Terraform configuration to enable `firestore.googleapis.com` and, more importantly, I had to assign the right roles to my application's Service Account:
- `roles/mcp.toolUser`: This is the key that lets the agent actually "talk" to the MCP server.
- `roles/datastore.user`: Standard permissions to read the data.

I also had to explicitly enable the MCP server for my project using the `gcloud` CLI:
```bash
gcloud beta services mcp enable firestore.googleapis.com
```

## Phase 2: First Contact and the "405 Trap"

This is where the theory met the cold, hard reality of HTTP status codes. My initial implementation used the ADK’s `SseConnectionParams`. It seemed logical — MCP often uses Server-Sent Events (SSE) for its transport. 

However, the moment I sent my first "Hello" to the chatbot, the backend exploded with a `405 Method Not Allowed`. 

### The Discovery:
The managed Firestore MCP endpoint (`https://firestore.googleapis.com/mcp`) requires a **POST** request to initiate the SSE session. The standard `SseConnectionParams` in the SDK defaults to a **GET** request.

### The Fix:
I switched to `StreamableHTTPConnectionParams`. This specific parameter class is designed for endpoints that require a bit more "handshaking" — like a POST request — to get the stream flowing.

## Phase 3: The Freshness Factor (Authentication)

Authentication was the next hurdle. Initially, I was grabbing a token at startup and passing it into the headers. Great for the first 60 minutes; disastrous for the 61st. 

### The Fix:
I implemented a `header_provider` callback. This is a brilliant feature of the `McpToolset` that allows the agent to call a function every time it needs to talk to the MCP server. I wired this up to `google.auth` to ensure that every request carries a fresh, valid OAuth2 token. This is the "proper" way to handle long-running agent sessions in a secure environment.

## Phase 4: The Schema Showstopper

We were so close. The connection was alive, the tokens were fresh, and then... I asked the chatbot: *"How many blogs do you have?"*

**Crash.** `RuntimeError: Invalid structured content returned by tool list_documents`.

### The Critical Discovery:
The managed Firestore MCP server has a strict schema bug. When a field in Firestore is empty (like an optional `author_url`), the server returns a literal JSON `null`. However, the tool's official schema defines that field as an enum that *must* be the string `"NULL_VALUE"`. 

I managed to isolate this behavior using a bespoke diagnostic script, `scripts/test_mcp_bug.py`, which allowed me to inspect the raw tool definitions and responses coming back from the MCP server without the ADK's validation layer getting in the way. It confirmed that the server was sending back JSON that violated its own contract.

Because the ADK uses strict Pydantic/jsonschema validation, it sees the `null` and essentially says, "I wasn't expecting that," and shuts down the session. It’s a classic case of a server not following its own rules.

## Phase 5: The Monkey-Patching Maneuver (Survival of the Pragmatic)

I was stuck. The server-side bug was out of my control, and the client-side library was too pedantic to ignore it. As an architect, I had two choices: give up on MCP entirely, or find a way to make the library "look the other way."

I chose the latter. I implemented a **Monkey-Patch** at the very top of my `app/agent.py`. By overwriting the internal validation method of the MCP `ClientSession`, I effectively told the agent: *"Trust me, just give me the raw data."*

```python
import mcp.client.session

# Disabling strict validation to handle the server-side schema bug.
# Note: This must be an async function to satisfy the SDK's expectations.
async def _skip_validation(self, name, result):
    return None

mcp.client.session.ClientSession._validate_tool_result = _skip_validation
```

Total success. The crashes stopped immediately. Gemini, being the powerhouse that it is, has no problem seeing a `null` in the JSON response and continuing its reasoning loop.

## The Hybrid Verdict: Why Bespoke Still Matters

With the monkey-patch in place, technically the generic `list_documents` tool works. So, did I delete my bespoke search tool? **Absolutely not.**

I’ve adopted a **Hybrid Architecture**, and here is the architectural reasoning:

1.  **Context Efficiency**: If I use the generic `list_documents` tool for a broad search, the server returns the **full document content** for every single item. Dumping 100+ full blog posts into the LLM's context window just to answer "Do you have any Python blogs?" is a massive waste of tokens and a sure way to hit context limits. My bespoke `search_portfolio` tool returns only concise summaries and IDs.
2.  **Search Intelligence**: My bespoke tool knows how to properly scan array-based tags and AI-generated summaries. Generic MCP tools are "dumb" lists — they don't have the application-specific matching logic that makes an agent feel "smart."
3.  **The "Counting" Problem**: Accurate counting (e.g., "How many blogs?") is instantaneous with a tiny bit of Python logic but slow and error-prone if an LLM has to count a raw JSON list manually.

## So, Why Keep MCP at All?

You might be thinking: *"Dazbo, if you're keeping your old search tool, why bother with MCP?"*

It’s about **Surgical Retrieval** and **Standardisation**.

- **ROI on Precision**: For fetching the full Markdown body of a specific project (via `get_document`), MCP is perfect. I don't have to maintain any retrieval logic; Google does it for me.
- **Portability**: My agent now speaks a standard protocol for its core data access. If I want to add more managed Google tools later (like BigQuery or Sheets), the pattern is already established.
- **Future-Proofing**: If Google releases a new Firestore-native tool tomorrow — say, a specialized vector search — my agent gets it for "free" via discovery, without me writing another bespoke Python tool.

## Final Summary of Discoveries

| Problem | Discovery | Fix |
| :--- | :--- | :--- |
| **405 Method Not Allowed** | Endpoint requires POST, not GET. | Used `StreamableHTTPConnectionParams`. |
| **Token Expiry** | Static tokens die after 1 hour. | Implemented `header_provider` callback. |
| **Client Crashes on Search** | Server-side `null` vs `"NULL_VALUE"` bug. | **Monkey-Patched** the MCP validation logic. |
| **Context Bloat** | Generic list tools are too verbose. | Pivoted to **Hybrid Tooling** (Bespoke Search + MCP Retrieval). |

## Wrapping Up

This journey was a lot more "scenic" than I expected, but the resulting architecture is rock-solid. We’ve combined the strengths of a managed, standard protocol with the precision of bespoke code. It’s pragmatic, it’s efficient, and it’s very "Dazbo."

Until next time, keep your tokens fresh and your dashes spaced!

---
*Darren "Dazbo" Lester is an Enterprise Cloud Architect who probably spends way too much time obsessing over the spacing of em-dashes.*
