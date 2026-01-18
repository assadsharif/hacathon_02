# Phase II Plan — Hackathon II

## Strategy
Incrementally layer web architecture over Phase I logic.

## Milestones

### M1: Backend Foundation
- FastAPI app scaffold
- SQLModel schema aligned with Phase I
- Neon DB connection

### M2: API Parity
- REST endpoints for all Phase I actions
- Validation rules preserved

### M3: Frontend Foundation
- Next.js App Router
- API client abstraction
- Todo pages: list view, create form, update form

### M4: End-to-End Flow
- UI → API → DB → UI
- Error handling (network errors, validation errors, server errors)
- Loading states (API call pending, optimistic updates)
- Empty states (no todos, error messages)

### M5: Authentication & User-Scoped Data (NEW)
- Better Auth integration with Next.js
- User registration and sign-in pages
- JWT token issuance and verification
- Backend middleware for JWT validation
- Database migration: add users table and user_id to todos
- User-scoped todo filtering (all queries filtered by authenticated user)
- Protected routes and API endpoints

## Risk Controls
- Specs reviewed before each milestone
- No frontend logic duplication
- No DB logic in frontend

## Completion Criteria
- Fresh install runs locally
- Phase I still works untouched
- Phase II passes manual acceptance checks
- All todo operations require authentication
- Users see only their own todos (data isolation verified)

---

## Authentication Architecture (M5)

### Overview
Better Auth provides production-ready authentication for Next.js with JWT token support. The frontend issues JWT tokens on sign-in, and the backend verifies these tokens on every API request.

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Sign-Up     │  │   Sign-In    │  │  Better Auth    │   │
│  │  Page        │  │   Page       │  │  Client         │   │
│  │  /sign-up    │  │   /sign-in   │  │  (with MCP)     │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘   │
│         │                  │                   │             │
│         └──────────────────┴───────────────────┘             │
│                            │                                 │
│                   ┌────────▼────────┐                        │
│                   │  JWT Token      │                        │
│                   │  Storage        │                        │
│                   │  (Session)      │                        │
│                   └────────┬────────┘                        │
│                            │                                 │
│         ┌──────────────────▼──────────────────┐             │
│         │     API Client (lib/api.ts)         │             │
│         │  - Attaches JWT to Authorization    │             │
│         │  - Header: Bearer <token>           │             │
│         └──────────────────┬──────────────────┘             │
└────────────────────────────┼──────────────────────────────┘
                             │ HTTP + JWT
                             │
┌────────────────────────────▼──────────────────────────────┐
│                    BACKEND (FastAPI)                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │          JWT Verification Middleware                │  │
│  │  1. Extract Authorization header                    │  │
│  │  2. Verify JWT signature with secret                │  │
│  │  3. Extract user_id from claims                     │  │
│  │  4. Attach user_id to request context               │  │
│  └─────────────────────┬───────────────────────────────┘  │
│                        │                                   │
│         ┌──────────────▼──────────────┐                   │
│         │   Protected API Endpoints   │                   │
│         │  - GET /api/todos            │                   │
│         │  - POST /api/todos           │                   │
│         │  - PUT /api/todos/{id}       │                   │
│         │  - DELETE /api/todos/{id}    │                   │
│         │  All filtered by user_id     │                   │
│         └──────────────┬────────────────┘                  │
│                        │                                   │
│  ┌─────────────────────▼───────────────────────────────┐  │
│  │            Database Queries (SQLModel)              │  │
│  │  WHERE user_id = <authenticated_user_id>            │  │
│  └─────────────────────┬───────────────────────────────┘  │
└────────────────────────┼──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│                DATABASE (Neon PostgreSQL)                  │
│  ┌──────────────┐         ┌──────────────────────────┐   │
│  │    users     │         │        todos             │   │
│  ├──────────────┤         ├──────────────────────────┤   │
│  │ id (PK)      │◄────────│ user_id (FK) ← NEW       │   │
│  │ email        │         │ id (PK)                  │   │
│  │ password_hash│         │ title                    │   │
│  │ name         │         │ description              │   │
│  │ created_at   │         │ status                   │   │
│  └──────────────┘         │ created_at               │   │
│                           │ updated_at               │   │
│  Better Auth tables:      └──────────────────────────┘   │
│  - session                                                │
│  - account                                                │
│  - verification                                           │
└───────────────────────────────────────────────────────────┘
```

### Data Flow

**Registration Flow:**
1. User submits email/password on `/sign-up`
2. Frontend calls Better Auth registration endpoint
3. Better Auth creates user in database with hashed password
4. User redirected to `/sign-in`

**Sign-In Flow:**
1. User submits credentials on `/sign-in`
2. Better Auth verifies password against hash
3. Better Auth issues JWT with claims: `{user_id, email, iat, exp}`
4. JWT stored in Better Auth session (cookie + state)
5. User redirected to `/todos`

**Authenticated API Request Flow:**
1. Frontend API client reads JWT from Better Auth session
2. API client attaches JWT to Authorization header: `Bearer <token>`
3. Backend middleware intercepts request
4. Middleware verifies JWT signature using shared secret
5. Middleware extracts `user_id` from verified claims
6. Middleware attaches `user_id` to request context
7. API endpoint handler uses `user_id` to filter database queries
8. Response sent back with only user's own data

**Sign-Out Flow:**
1. User clicks sign-out button
2. Frontend calls Better Auth sign-out
3. Better Auth clears session and JWT
4. User redirected to `/sign-in`

### Security Model

**Token Security:**
- JWT signed with HS256 (HMAC-SHA256)
- Secret key: 256-bit minimum (stored in environment variable)
- Token includes expiration (7 days default)
- Backend verifies signature on every request

**Password Security:**
- Passwords hashed using bcrypt/argon2 (Better Auth default)
- Plain text passwords NEVER stored
- Password validation: minimum 8 characters

**Data Isolation:**
- Database queries ALWAYS include `WHERE user_id = <authenticated_user_id>`
- Users cannot see or modify other users' todos
- Attempting to access another user's todo returns 404 (not 403, to avoid enumeration)

**Error Handling:**
- Invalid JWT → 401 Unauthorized
- Expired JWT → 401 Unauthorized
- Missing JWT → 401 Unauthorized
- Frontend catches 401 responses and redirects to `/sign-in`

### Database Schema Changes

**New Users Table:**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Migration for Todos Table:**
```sql
ALTER TABLE todos
ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE CASCADE;

-- Set user_id for existing todos (choose strategy):
-- Option 1: Assign to first registered user
-- Option 2: Delete existing todos
-- Option 3: Create a "migration" user

CREATE INDEX idx_todos_user_id ON todos(user_id);
```

**Better Auth Tables** (auto-created by Better Auth):
- `session`: Active user sessions
- `account`: OAuth accounts (unused, but required by schema)
- `verification`: Email verification tokens (unused in Phase II)

### Frontend Implementation

**Better Auth Configuration:**
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { mcp } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    mcp({
      loginPage: "/sign-in"
    })
  ],
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET,
    expiresIn: "7d"
  }
});
```

**API Client Enhancement:**
```typescript
// lib/api.ts (updated)
export class TodoApi {
  private async getAuthHeader(): Promise<string | null> {
    const session = await getSession(); // Better Auth session
    if (!session?.token) return null;
    return `Bearer ${session.token}`;
  }

  async listTodos(...) {
    const authHeader = await this.getAuthHeader();
    const response = await fetch(url, {
      headers: {
        'Authorization': authHeader
      }
    });
    // Handle 401 → redirect to sign-in
  }
}
```

**Protected Route Wrapper:**
```typescript
// middleware.ts or layout component
if (!session) {
  redirect('/sign-in');
}
```

### Backend Implementation

**JWT Verification Middleware:**
```python
# backend/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

async def get_current_user_id(
    credentials: HTTPAuthCredentials = Depends(security)
) -> str:
    """Extract and verify JWT, return user_id"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Updated API Endpoints:**
```python
# backend/routers/todos.py (updated)
@router.get("/", response_model=List[TodoResponse])
async def list_todos(
    user_id: str = Depends(get_current_user_id),  # NEW
    session: Session = Depends(get_session)
):
    query = select(Todo).where(Todo.user_id == user_id)  # NEW
    todos = session.exec(query).all()
    return todos

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo_data: TodoCreate,
    user_id: str = Depends(get_current_user_id),  # NEW
    session: Session = Depends(get_session)
):
    todo = Todo(**todo_data.model_dump(), user_id=user_id)  # NEW
    # ... rest of logic
```

### Environment Variables

**Frontend (.env.local):**
```bash
BETTER_AUTH_SECRET=93457b5f5d59fd9d65726648e22a4e28
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env):**
```bash
JWT_SECRET=93457b5f5d59fd9d65726648e22a4e28
DATABASE_URL=postgresql://...
```

### Testing Strategy

**Unit Tests:**
- JWT verification function
- User-scoped query filtering
- Password hashing

**Integration Tests:**
- Full registration → sign-in → API request flow
- Cross-user data isolation
- 401 handling on invalid/expired tokens

**Manual Tests:**
- Create two users, verify data isolation
- Sign out and verify redirect to sign-in
- Try to access protected page when signed out

---

## Technical Decisions

### Why Better Auth over NextAuth?
- Native Next.js App Router support
- MCP plugin for easy integration
- Built-in JWT support
- Simpler configuration
- Active development and modern API

### Why JWT over Sessions?
- Stateless backend (no session storage needed)
- Works well with serverless architecture (Neon)
- Frontend can inspect token contents
- Better Auth handles both JWT + session cookie

### Why HS256 (symmetric) over RS256 (asymmetric)?
- Simpler setup (single secret key)
- Sufficient for single-service architecture
- Better Auth default
- Can upgrade to RS256 if needed for microservices

### Why user_id in JWT claims?
- Enables efficient filtering without database lookup
- Stateless authentication
- Standard practice for user-scoped APIs
