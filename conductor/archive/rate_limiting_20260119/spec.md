# Specification - Rate Limiting for Cost & DoS Control

## Overview
Implement a lightweight rate limiting mechanism for the portfolio application to manage LLM costs (Gemini API) and protect against simple Denial of Service (DoS) attacks. We will use a process-local, in-memory approach using the `slowapi` library (or similar FastAPI-compatible tool) to avoid adding Redis or other infrastructure.

## Functional Requirements
- **Backend Implementation:**
    - Integrate `slowapi` into the FastAPI application.
    - **Global Limit:** Apply a baseline rate limit to all endpoints under `/api` (e.g., 60 requests per minute).
    - **Agent Limit:** Apply a strict limit specifically to the chat/agent endpoint (e.g., 5 requests per minute) to control costs.
    - **Exemptions:** Ensure health checks and static frontend assets are not subject to rate limiting.
    - **Client Identification:** Use the standard remote address (client IP) as the key for rate limiting.
- **Frontend Handling:**
    - Update the `ChatWidget.tsx` to detect HTTP 429 (Too Many Requests) responses.
    - Display a user-friendly message (e.g., "You're sending messages too fast. Please wait a moment.") when the limit is hit.
    - Ensure general API services in React handle 429 errors gracefully (e.g., via toasts or console warnings).

## Non-Functional Requirements
- **Performance:** Rate limiting checks should have negligible impact on API response latency.
- **Simplicity:** No new infrastructure (like Redis) should be required; storage remains in-memory.

## Acceptance Criteria
- [ ] API requests exceeding the defined thresholds return an HTTP 429 status code.
- [ ] The Chat Widget displays a clear, friendly error message when the agent limit is exceeded.
- [ ] Static assets (JS, CSS, images) remain accessible even if the API rate limit is reached.
- [ ] Unit tests verify that the rate limiter correctly increments counts and triggers at the expected thresholds.

## Out of Scope
- Distributed rate limiting (limits are tracked per Cloud Run instance).
- Sophisticated bot detection or WAF-level protection.
- Authenticated user-specific quotas.
