# Specification: Firestore Migration and Schema Definition

## Overview
The goal of this track is to replace the existing PostgreSQL/asyncpg database layer with Google Firestore. This transition aligns with the desire for a serverless, managed database solution that simplifies infrastructure management for the Dazbo Portfolio application.

## Requirements
- Replace `asyncpg` with `google-cloud-firestore`.
- Define a NoSQL schema suitable for portfolio content (projects, blogs, experience).
- Implement a session service for the ADK agent that uses Firestore for persistence.
- Update the FastAPI application to use the new Firestore services.
- Ensure high test coverage (>80%) for the new data layer.

## Data Models (Proposed)

### Collection: `projects`
- `id`: string (auto-generated)
- `title`: string
- `description`: string
- `tags`: list[string]
- `repo_url`: string (optional)
- `demo_url`: string (optional)
- `image_url`: string (optional)
- `featured`: boolean
- `created_at`: timestamp

### Collection: `blogs`
- `id`: string (auto-generated)
- `title`: string
- `summary`: string
- `date`: string (ISO 8601)
- `platform`: string (e.g., Medium, Hashnode)
- `url`: string
- `created_at`: timestamp

### Collection: `experience`
- `id`: string (auto-generated)
- `company`: string
- `role`: string
- `duration`: string (e.g., "Jan 2020 - Present")
- `description`: string
- `skills`: list[string]
- `order`: integer (for sorting)

### Collection: `sessions`
- `id`: string (session_id)
- `user_id`: string
- `state`: map (ADK session state)
- `events`: list (ADK session events)
- `updated_at`: timestamp

## Technical Architecture
1. **Model Layer:** Use Pydantic models for data validation and Firestore document mapping.
2. **Service Layer:** A `FirestoreService` base class to encapsulate common Firestore operations (get, list, create, update, delete). Specialized services (e.g., `ProjectService`) will inherit from this.
3. **Session Service:** A custom implementation of ADK's `BaseSessionService` using Firestore.
4. **Integration:** Update FastAPI dependency injection to provide Firestore services to routes.
