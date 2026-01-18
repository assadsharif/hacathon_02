# Todo API Documentation
**[Task]: AUTH-D6**
**Version**: 2.0.0 (with Authentication)
**Last Updated**: 2026-01-12

This API provides CRUD operations for todo items with JWT-based authentication.

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Error Responses](#error-responses)
4. [Examples](#examples)

---

## Authentication

### Overview

All `/api/todos/*` endpoints require JWT authentication. The API uses:

- **Token Type**: JWT (JSON Web Tokens)
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Header Format**: `Authorization: Bearer <token>`
- **Token Expiration**: 7 days
- **Token Claims**: `user_id`, `email`, `iat`, `exp`

### Obtaining a Token

Tokens are issued by Better Auth on the frontend:

1. **Register**: POST to `/api/auth/sign-up`
2. **Sign In**: POST to `/api/auth/sign-in/email`

After authentication, Better Auth stores the token in a session cookie and your frontend API client automatically includes it in requests.

### Using Tokens

Include the JWT token in the `Authorization` header of every request:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Security Notes

- **User-Scoped Data**: All todo operations are automatically filtered by the authenticated user's ID
- **Data Isolation**: Users cannot access, modify, or delete other users' todos
- **401 Responses**: Missing or invalid tokens return `401 Unauthorized`
- **404 Responses**: Attempting to access another user's todo returns `404 Not Found` (prevents data leakage)

---

## Endpoints

Base URL: `http://localhost:8000` (development)

### 1. List Todos

Get all todos for the authenticated user.

**Endpoint**: `GET /api/todos`

**Authentication**: Required ✅

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status_filter` | string | No | Filter by status: `"active"` or `"completed"` |

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Complete Phase II implementation",
    "description": "Add authentication feature",
    "status": "active",
    "created_at": "2026-01-11T12:00:00",
    "updated_at": "2026-01-11T12:00:00"
  }
]
```

**Example**:
```bash
curl -H "Authorization: Bearer <your_token>" \
     http://localhost:8000/api/todos

# With status filter
curl -H "Authorization: Bearer <your_token>" \
     "http://localhost:8000/api/todos?status_filter=active"
```

---

### 2. Get Todo

Get a single todo by ID (must be owned by authenticated user).

**Endpoint**: `GET /api/todos/{todo_id}`

**Authentication**: Required ✅

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todo_id` | integer | Yes | Todo ID |

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete Phase II implementation",
  "description": "Add authentication feature",
  "status": "active",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:00:00"
}
```

**Errors**:
- `404 Not Found` - Todo not found or not owned by user

**Example**:
```bash
curl -H "Authorization: Bearer <your_token>" \
     http://localhost:8000/api/todos/1
```

---

### 3. Create Todo

Create a new todo (automatically assigned to authenticated user).

**Endpoint**: `POST /api/todos`

**Authentication**: Required ✅

**Request Body**:
```json
{
  "title": "Complete Phase II implementation",
  "description": "Add authentication feature",
  "status": "active"
}
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Todo title (1-200 characters) |
| `description` | string | No | Optional description |
| `status` | string | No | Status: `"active"` (default) or `"completed"` |

**Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete Phase II implementation",
  "description": "Add authentication feature",
  "status": "active",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:00:00"
}
```

**Example**:
```bash
curl -X POST \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"title":"New Todo","status":"active"}' \
     http://localhost:8000/api/todos
```

---

### 4. Update Todo

Update an existing todo (must be owned by authenticated user).

**Endpoint**: `PUT /api/todos/{todo_id}`

**Authentication**: Required ✅

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todo_id` | integer | Yes | Todo ID |

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "created_at": "2026-01-11T12:00:00",
  "updated_at": "2026-01-11T12:30:00"
}
```

**Errors**:
- `404 Not Found` - Todo not found or not owned by user

**Example**:
```bash
curl -X PUT \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"status":"completed"}' \
     http://localhost:8000/api/todos/1
```

---

### 5. Delete Todo

Delete a todo (must be owned by authenticated user).

**Endpoint**: `DELETE /api/todos/{todo_id}`

**Authentication**: Required ✅

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todo_id` | integer | Yes | Todo ID |

**Response**: `204 No Content`

**Errors**:
- `404 Not Found` - Todo not found or not owned by user

**Example**:
```bash
curl -X DELETE \
     -H "Authorization: Bearer <your_token>" \
     http://localhost:8000/api/todos/1
```

---

## Error Responses

### 401 Unauthorized

**Cause**: Missing, invalid, or expired JWT token

**Response**:
```json
{
  "detail": "Invalid token: <error_message>"
}
```

**Common errors**:
- `"Invalid token: missing user_id claim"` - Token doesn't contain user_id
- `"Invalid token: Signature verification failed"` - Token signature invalid
- `"Invalid token: Token is expired"` - Token expired (> 7 days old)
- `"Authentication required. Please sign in."` - No Authorization header

**Solution**: Sign in again to get a new token

---

### 404 Not Found

**Cause**: Todo doesn't exist or is owned by another user

**Response**:
```json
{
  "detail": "Todo with id 1 not found"
}
```

**Security Note**: The API returns the same 404 response whether:
- The todo doesn't exist, OR
- The todo exists but is owned by another user

This prevents attackers from discovering which todo IDs exist in the system.

---

### 422 Validation Error

**Cause**: Invalid request data

**Response**:
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

**Common validation errors**:
- Missing required field (`title`)
- Invalid status value (must be `"active"` or `"completed"`)
- Title too long (> 200 characters)

---

## Examples

### Complete Workflow

#### 1. Register a New User (Frontend)

```bash
# This is handled by Better Auth on frontend
# POST /api/auth/sign-up
# Returns JWT token in session cookie
```

#### 2. Create a Todo

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy groceries",
       "description": "Milk, eggs, bread",
       "status": "active"
     }' \
     http://localhost:8000/api/todos
```

#### 3. List All Todos

```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/todos
```

#### 4. Update Todo Status

```bash
curl -X PUT \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}' \
     http://localhost:8000/api/todos/1
```

#### 5. Delete Completed Todos

```bash
# First get all completed todos
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/todos?status_filter=completed"

# Then delete each one
curl -X DELETE \
     -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/todos/1
```

---

## Testing with curl

### Get JWT Token from Browser

1. Sign in to the app at http://localhost:3000/sign-in
2. Open DevTools → Application → Cookies
3. Copy the value of `better-auth.session_token`
4. Use it in curl commands:

```bash
export TOKEN="your_token_here"

# Now you can use $TOKEN in requests
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/todos
```

---

## Rate Limiting

**Status**: Not implemented yet

Future versions may include rate limiting:
- 100 requests per minute per user
- 429 Too Many Requests response when exceeded

---

## Changelog

### Version 2.0.0 (2026-01-12)
- ✅ Added JWT authentication to all endpoints
- ✅ Added `user_id` field to todo responses
- ✅ Implemented user-scoped data filtering
- ✅ Added 401 Unauthorized responses
- ✅ Updated security model (data isolation)

### Version 1.0.0 (2026-01-11)
- Initial release (Phase I)
- CRUD operations for todos
- No authentication (all todos public)

---

## Additional Resources

- **Better Auth Documentation**: https://www.better-auth.com/docs
- **JWT Introduction**: https://jwt.io/introduction
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/

---

## Support

For issues or questions:
- Check the Testing Guide: `../TESTING_GUIDE.md`
- Review authentication spec: `../specs/phase-ii/authentication.spec.md`
- Check implementation log: `../specs/phase-ii/IMPLEMENTATION_LOG.md`
