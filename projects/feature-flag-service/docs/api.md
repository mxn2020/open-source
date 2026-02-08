# API Reference

Base URL: `http://localhost:8000`

## Authentication

Admin endpoints require an `X-API-Key` header. The key is configured via the `FF_API_KEY`
environment variable (default: `dev-api-key` for development).

```
X-API-Key: your-secret-key
```

## Endpoints

### Health Check

**`GET /health`**

Returns the service health status.

**Response** `200 OK`

```json
{
  "status": "healthy"
}
```

---

### Create a Feature Flag

**`POST /api/flags`** *(requires authentication)*

**Request Body**

| Field       | Type     | Required | Default | Description                    |
| ----------- | -------- | -------- | ------- | ------------------------------ |
| name        | string   | yes      |         | Unique flag name               |
| description | string   | no       | `""`    | Description of the flag        |
| enabled     | boolean  | no       | `false` | Whether the flag is enabled    |
| percentage  | integer  | no       | `100`   | Rollout percentage (0-100)     |
| tags        | string[] | no       | `[]`    | Tags for filtering             |

**Response** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "dark-mode",
  "description": "Enable dark mode UI",
  "enabled": true,
  "percentage": 100,
  "tags": ["ui", "beta"],
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

**Errors**

| Status | Description               |
| ------ | ------------------------- |
| 401    | Missing or invalid API key|
| 409    | Flag name already exists  |

---

### List Feature Flags

**`GET /api/flags`**

**Query Parameters**

| Parameter | Type   | Required | Description            |
| --------- | ------ | -------- | ---------------------- |
| tag       | string | no       | Filter flags by tag    |

**Response** `200 OK`

```json
[
  {
    "id": "...",
    "name": "dark-mode",
    "description": "Enable dark mode UI",
    "enabled": true,
    "percentage": 100,
    "tags": ["ui", "beta"],
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

---

### Get a Feature Flag

**`GET /api/flags/{name}`**

**Path Parameters**

| Parameter | Type   | Description        |
| --------- | ------ | ------------------ |
| name      | string | The flag name      |

**Response** `200 OK`

Returns a single feature flag object.

**Errors**

| Status | Description     |
| ------ | --------------- |
| 404    | Flag not found  |

---

### Update a Feature Flag

**`PUT /api/flags/{name}`** *(requires authentication)*

**Path Parameters**

| Parameter | Type   | Description        |
| --------- | ------ | ------------------ |
| name      | string | The flag name      |

**Request Body** (all fields optional)

| Field       | Type     | Description                    |
| ----------- | -------- | ------------------------------ |
| name        | string   | New flag name                  |
| description | string   | New description                |
| enabled     | boolean  | New enabled state              |
| percentage  | integer  | New rollout percentage (0-100) |
| tags        | string[] | New tags                       |

**Response** `200 OK`

Returns the updated feature flag object.

**Errors**

| Status | Description               |
| ------ | ------------------------- |
| 401    | Missing or invalid API key|
| 404    | Flag not found            |

---

### Delete a Feature Flag

**`DELETE /api/flags/{name}`** *(requires authentication)*

**Path Parameters**

| Parameter | Type   | Description        |
| --------- | ------ | ------------------ |
| name      | string | The flag name      |

**Response** `204 No Content`

**Errors**

| Status | Description               |
| ------ | ------------------------- |
| 401    | Missing or invalid API key|
| 404    | Flag not found            |

---

### Evaluate a Feature Flag

**`POST /api/evaluate`**

Evaluate whether a flag is enabled for a specific user. Uses percentage-based rollout
with consistent hashing when a `user_id` is provided.

**Request Body**

| Field     | Type   | Required | Description                           |
| --------- | ------ | -------- | ------------------------------------- |
| flag_name | string | yes      | The flag to evaluate                  |
| user_id   | string | no       | User ID for percentage-based rollout  |

**Response** `200 OK`

```json
{
  "flag_name": "dark-mode",
  "enabled": true,
  "reason": "User is in rollout group (50%)"
}
```

**Evaluation Logic**

1. If the flag does not exist, returns `enabled: false` with reason "Flag not found".
2. If the flag is disabled (`enabled: false`), returns `enabled: false`.
3. If the flag is enabled with 100% rollout, returns `enabled: true`.
4. If the flag is enabled with 0% rollout, returns `enabled: false`.
5. If a `user_id` is provided, the user is hashed into a bucket (0-99). If the bucket
   is less than the flag's percentage, the user is in the rollout group.
6. If no `user_id` is provided for a partial rollout, returns `enabled: true` with a note.
