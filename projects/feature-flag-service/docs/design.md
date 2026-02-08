# Design

This document describes the architecture and design decisions behind the Feature Flag Service.

## Overview

The Feature Flag Service is a lightweight REST API for managing feature flags. It is designed
to be simple to deploy and operate, with minimal dependencies and no external database
requirements.

## Architecture

```
┌──────────────┐     ┌─────────────┐     ┌────────────┐
│   Client     │────▶│  FastAPI     │────▶│  SQLite    │
│  (httpx/curl)│◀────│  Routes      │◀────│  Database  │
└──────────────┘     └─────────────┘     └────────────┘
                           │
                      ┌────┴─────┐
                      │ Auth     │
                      │ Middleware│
                      └──────────┘
```

### Components

- **FastAPI Application** (`app.py`): Entry point that configures the application, CORS
  middleware, and database initialization via the lifespan context manager.
- **Routes** (`routes.py`): Defines all HTTP endpoints. Uses FastAPI dependency injection
  for database access and authentication.
- **Models** (`models.py`): Pydantic models for request validation, response serialization,
  and internal data representation.
- **Database** (`database.py`): SQLite-backed storage layer using Python's built-in `sqlite3`
  module. Handles all CRUD operations and flag evaluation logic.
- **Auth** (`auth.py`): Simple API key authentication. Admin endpoints require a valid
  `X-API-Key` header matching the `FF_API_KEY` environment variable.

## Design Decisions

### SQLite Storage

SQLite was chosen for simplicity. It requires no separate database server, is included in
Python's standard library, and provides ACID transactions. For production use at scale,
the database layer could be swapped for PostgreSQL or another backend.

### Percentage Rollouts

Percentage-based rollouts use SHA-256 hashing of `flag_name:user_id` to assign users to a
bucket from 0-99. This approach provides:

- **Consistency**: The same user always gets the same result for a given flag.
- **Uniformity**: SHA-256 provides good distribution across buckets.
- **Independence**: Different flags produce different bucket assignments for the same user.

### Authentication Model

A simple API key model was chosen over OAuth or JWT for simplicity. Read operations
(list, get, evaluate) are unauthenticated to allow easy integration with client-side code.
Write operations (create, update, delete) require authentication.

### CORS

CORS is configured to allow all origins by default for development convenience. In production,
this should be restricted to specific allowed origins.

## Data Model

### Feature Flag

| Field       | Type       | Description                                      |
| ----------- | ---------- | ------------------------------------------------ |
| id          | UUID       | Auto-generated unique identifier                 |
| name        | string     | Unique flag name (used as lookup key)             |
| description | string     | Human-readable description                        |
| enabled     | boolean    | Whether the flag is active                        |
| percentage  | int (0-100)| Rollout percentage for gradual releases           |
| tags        | string[]   | Labels for organization and filtering             |
| created_at  | datetime   | Creation timestamp (UTC)                          |
| updated_at  | datetime   | Last update timestamp (UTC)                       |
