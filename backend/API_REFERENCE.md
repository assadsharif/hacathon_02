# API Reference - Todo API

Base URL: `http://localhost:8000`

## Health Endpoints

### GET /
Get API information

**Response:**
```json
{
  "message": "Todo API - Phase II",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

### GET /health
Health check

**Response:**
```json
{
  "status": "healthy",
  "service": "todo-api",
  "version": "1.0.0"
}
```

### GET /health/db
Database connectivity check

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Database connection successful"
}
```

---

## Todo Endpoints

### GET /api/todos
List all todos with optional status filter

**Query Parameters:**
- `status_filter` (optional): `"active"` or `"completed"`

**Examples:**
```bash
# Get all todos
GET /api/todos

# Get only active todos
GET /api/todos?status_filter=active

# Get only completed todos
GET /api/todos?status_filter=completed
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Complete Phase II implementation",
    "description": "Add description field for Phase I compatibility",
    "status": "active",
    "created_at": "2026-01-11T12:00:00",
    "updated_at": "2026-01-11T12:00:00"
  },
  {
    "id": 2,
    "title": "Write documentation",
    "description": "Update API reference and validation reports",
    "status": "completed",
    "created_at": "2026-01-11T12:05:00",
    "updated_at": "2026-01-11T12:10:00"
  }
]
```

---

### GET /api/todos/{id}
Get a single todo by ID

**Path Parameters:**
- `id` (required): Todo ID (integer)

**Example:**
```bash
GET /api/todos/1
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Complete Phase II implementation",
  "description": "Add description field for Phase I compatibility",
  "status": "active",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:00:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Todo with id 999 not found"
}
```

---

### POST /api/todos
Create a new todo

**Request Body:**
```json
{
  "title": "Complete Phase II implementation",
  "description": "Add description field for Phase I compatibility",  // optional, defaults to null
  "status": "active"  // optional, defaults to "active"
}
```

**Validation:**
- `title`: Required, 1-200 characters
- `description`: Optional, any string or null (Phase I compatibility)
- `status`: Optional, must be `"active"` or `"completed"`

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Complete Phase II implementation",
  "description": "Add description field for Phase I compatibility",
  "status": "active",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:00:00"
}
```

**Error Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### PUT /api/todos/{id}
Update an existing todo (partial update supported)

**Path Parameters:**
- `id` (required): Todo ID (integer)

**Request Body (all fields optional):**
```json
{
  "title": "Updated title",         // optional
  "description": "Updated desc",    // optional
  "status": "completed"             // optional
}
```

**Examples:**
```bash
# Update only status
PUT /api/todos/1
{
  "status": "completed"
}

# Update only title
PUT /api/todos/1
{
  "title": "New title"
}

# Update all fields
PUT /api/todos/1
{
  "title": "New title",
  "description": "New description",
  "status": "completed"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:15:00"  // automatically updated
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Todo with id 999 not found"
}
```

---

### DELETE /api/todos/{id}
Delete a todo

**Path Parameters:**
- `id` (required): Todo ID (integer)

**Example:**
```bash
DELETE /api/todos/1
```

**Response:** `204 No Content`
(No response body)

**Error Response:** `404 Not Found`
```json
{
  "detail": "Todo with id 999 not found"
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request succeeded (no response body) |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints interactively
- Download OpenAPI specification

---

## Testing

### Using curl

```bash
# List all todos
curl http://localhost:8000/api/todos

# Create a todo
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test todo", "description": "Test description", "status": "active"}'

# Get a todo
curl http://localhost:8000/api/todos/1

# Update a todo
curl -X PUT http://localhost:8000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated todo", "description": "Updated description", "status": "completed"}'

# Delete a todo
curl -X DELETE http://localhost:8000/api/todos/1
```

### Using test script

```bash
python test_crud_endpoints.py
```

---

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (Next.js frontend)
- `http://127.0.0.1:3000`

All HTTP methods and headers are allowed.
