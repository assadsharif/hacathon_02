# Phase II Specification — Hackathon II

## Objective
Transform the Phase I Todo system into a persistent, web-based application
while preserving its original domain rules and behaviors.

## Core Capabilities
- Web-based Todo CRUD
- Persistent storage using Neon Postgres
- REST API mirroring Phase I actions
- Stateless backend
- Deterministic behavior (same input → same output)

## User Roles
- Single User (Phase II scope)
- No multi-tenant logic yet

## Functional Requirements
- Create Todo
- List Todos
- Update Todo (status, title)
- Delete Todo
- Filter by status

## Non-Functional Requirements
- FastAPI must expose clean REST endpoints
  - RESTful HTTP verbs: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
  - Proper status codes: 200 (success), 201 (created), 404 (not found), 422 (validation error), 500 (server error)
  - JSON request/response format
  - Automatic OpenAPI documentation (FastAPI default)
  - Consistent error response structure: `{"detail": "error message"}`
- Next.js must consume API only (no direct DB)
- SQLModel mirrors Phase I models
- Environment-based config (.env file with DATABASE_URL)
- Clear separation of concerns (routes, models, database layer)

## Explicit Non-Goals
- AI features
- Auth complexity
- Realtime sync
- Background jobs
- Fancy UI polish

## Compatibility Rules
- Phase I logic is the reference behavior
- Phase II must behave identically at domain level
