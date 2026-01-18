# Feature Specification: User Authentication

**Feature ID**: AUTH-001
**Created**: 2026-01-12
**Status**: Draft
**Authority**: Phase II Constitution v1.1.0 Section VIII
**Input**: User request for Better Auth with JWT authentication

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P0)

As a new user, I want to create an account with email and password so I can securely access my todos.

**Why this priority**: Foundation for all authentication features. Without user registration, no one can use the application.

**Independent Test**: Can be tested by submitting registration form and verifying user is created in database with hashed password.

**Acceptance Scenarios**:

1. **Given** no existing account, **When** I register with email "user@example.com" and password "SecurePass123!", **Then** the system creates a user account, hashes the password, stores it in the database, and redirects me to the sign-in page
2. **Given** an existing account with email "user@example.com", **When** I try to register with the same email, **Then** the system displays error "Email already registered"
3. **Given** registration form, **When** I submit with invalid email format "notanemail", **Then** the system displays validation error "Invalid email format"
4. **Given** registration form, **When** I submit with weak password "123", **Then** the system displays error "Password must be at least 8 characters"

---

### User Story 2 - User Sign In (Priority: P0)

As a registered user, I want to sign in with my email and password so I can access my todos.

**Why this priority**: Required for users to access protected resources. Without sign-in, authentication is useless.

**Independent Test**: Can be tested by submitting credentials and verifying JWT token is issued and stored.

**Acceptance Scenarios**:

1. **Given** registered user with email "user@example.com" and password "SecurePass123!", **When** I sign in with correct credentials, **Then** the system issues a JWT token, stores it in Better Auth session, and redirects me to `/todos`
2. **Given** registered user, **When** I sign in with incorrect password, **Then** the system displays error "Invalid email or password"
3. **Given** non-existent user, **When** I try to sign in, **Then** the system displays error "Invalid email or password"
4. **Given** successful sign-in, **When** I navigate to protected pages, **Then** the JWT token is automatically included in API requests

---

### User Story 3 - Protected Todo Access (Priority: P0)

As a signed-in user, I want all my todo operations to be automatically authenticated so I only see my own todos.

**Why this priority**: Core security requirement. Ensures data isolation between users.

**Independent Test**: Can be tested by creating todos for different users and verifying each user only sees their own.

**Acceptance Scenarios**:

1. **Given** signed-in user A, **When** I create a todo "User A's task", **Then** the todo is associated with user A's ID and only visible to user A
2. **Given** signed-in user A with 5 todos, **When** I fetch todos, **Then** I see only my 5 todos, not todos from other users
3. **Given** signed-in user A, **When** I try to update user B's todo by ID, **Then** the system returns 404 Not Found (as if it doesn't exist)
4. **Given** signed-in user A, **When** I try to delete user B's todo by ID, **Then** the system returns 404 Not Found

---

### User Story 4 - User Sign Out (Priority: P1)

As a signed-in user, I want to sign out so I can end my session securely.

**Why this priority**: Important for security, especially on shared devices. Lower priority than core auth flows.

**Independent Test**: Can be tested by signing out and verifying session is cleared and JWT is invalidated.

**Acceptance Scenarios**:

1. **Given** signed-in user, **When** I click sign out, **Then** the system clears the JWT token, ends the session, and redirects me to `/sign-in`
2. **Given** signed-out user, **When** I try to access `/todos`, **Then** the system redirects me to `/sign-in`
3. **Given** signed-out user, **When** I make API request without JWT, **Then** the backend returns 401 Unauthorized

---

### User Story 5 - Unauthenticated Access Prevention (Priority: P0)

As the system, I want to prevent unauthenticated access to todo operations so data remains secure.

**Why this priority**: Critical security requirement. Without this, authentication is meaningless.

**Independent Test**: Can be tested by making API requests without JWT and verifying rejection.

**Acceptance Scenarios**:

1. **Given** no JWT token, **When** I try to access GET /api/todos, **Then** the backend returns 401 Unauthorized
2. **Given** expired JWT token, **When** I make API request, **Then** the backend returns 401 Unauthorized with error "Token expired"
3. **Given** invalid JWT token, **When** I make API request, **Then** the backend returns 401 Unauthorized with error "Invalid token"
4. **Given** unauthenticated user, **When** I try to access `/todos` page, **Then** the frontend redirects me to `/sign-in`

---

### Edge Cases

- What happens when JWT token expires during active session? System should detect 401 response and redirect to sign-in.
- How does the system handle concurrent sign-ins from multiple devices? Each device gets its own JWT token (Better Auth session management).
- What happens if database connection fails during authentication? Return 500 Internal Server Error with friendly message.
- How does the system prevent brute force attacks? Better Auth handles rate limiting (not in Phase II scope).
- What if user forgets password? Out of scope for Phase II (no password reset flow).

## Requirements *(mandatory)*

### Functional Requirements

**Authentication Flow:**
- **FR-AUTH-001**: System MUST provide user registration endpoint accepting email and password
- **FR-AUTH-002**: System MUST hash passwords using Better Auth defaults (bcrypt/argon2)
- **FR-AUTH-003**: System MUST validate email format and password strength (min 8 characters)
- **FR-AUTH-004**: System MUST prevent duplicate email registration
- **FR-AUTH-005**: System MUST provide sign-in endpoint returning JWT token on success
- **FR-AUTH-006**: System MUST validate credentials and reject invalid sign-in attempts
- **FR-AUTH-007**: System MUST issue JWT with user_id, email, iat, exp claims
- **FR-AUTH-008**: System MUST provide sign-out endpoint to invalidate session

**Authorization & Data Scoping:**
- **FR-AUTH-009**: System MUST verify JWT on all protected API endpoints
- **FR-AUTH-010**: System MUST extract user_id from verified JWT claims
- **FR-AUTH-011**: System MUST filter all todo queries by authenticated user_id
- **FR-AUTH-012**: System MUST reject API requests without valid JWT (401 Unauthorized)
- **FR-AUTH-013**: System MUST return 404 when user tries to access another user's todo
- **FR-AUTH-014**: System MUST associate new todos with authenticated user_id

**Frontend Integration:**
- **FR-AUTH-015**: Frontend MUST provide sign-up page at `/sign-up`
- **FR-AUTH-016**: Frontend MUST provide sign-in page at `/sign-in`
- **FR-AUTH-017**: Frontend MUST store JWT token via Better Auth session
- **FR-AUTH-018**: Frontend API client MUST automatically attach JWT to all requests
- **FR-AUTH-019**: Frontend MUST redirect unauthenticated users to `/sign-in`
- **FR-AUTH-020**: Frontend MUST handle 401 responses by redirecting to sign-in

### Key Entities

**User Entity** (new table):
```python
@dataclass
class User:
    id: str              # UUID primary key
    email: str           # Unique email address
    password_hash: str   # Hashed password (never plain text)
    name: str | None     # Optional display name
    created_at: datetime # Account creation timestamp
```

**Updated Todo Entity** (add user_id):
```python
@dataclass
class Todo:
    id: int                  # Existing primary key
    user_id: str             # NEW: Foreign key to User.id
    title: str               # Existing field
    description: str | None  # Existing field
    status: str              # Existing field (active/completed)
    created_at: datetime     # Existing field
    updated_at: datetime     # Existing field
```

**JWT Token Structure**:
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "iat": 1673456789,
  "exp": 1674061589
}
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-AUTH-001**: Users can register new accounts with email/password in single operation
- **SC-AUTH-002**: 100% of passwords are hashed (never stored as plain text)
- **SC-AUTH-003**: Users can sign in and receive valid JWT token
- **SC-AUTH-004**: 100% of todo API requests require valid JWT (no anonymous access)
- **SC-AUTH-005**: Users see ONLY their own todos (0% cross-user data leakage)
- **SC-AUTH-006**: Invalid/expired JWT tokens are rejected with 401 Unauthorized
- **SC-AUTH-007**: Frontend automatically handles authentication state (redirects to sign-in when needed)
- **SC-AUTH-008**: Users can sign out and JWT is properly invalidated

## Assumptions *(mandatory)*

1. **Better Auth Library**: Using Better Auth v1.0+ for Next.js with MCP plugin
2. **JWT Secret Management**: Secret key stored in environment variable (`.env.local` frontend, `.env` backend)
3. **Session Storage**: Better Auth uses database for session persistence
4. **Email Validation**: Basic format validation only (no email verification)
5. **Password Policy**: Minimum 8 characters (Better Auth default validation)
6. **Single Role**: All users have same permissions (no admin/user distinction)
7. **No Social Auth**: Email/password only (no OAuth providers)
8. **Token Expiration**: 7 days (Better Auth default)
9. **HTTPS**: Development uses HTTP, production requires HTTPS
10. **Database Support**: Neon PostgreSQL supports Better Auth schema

## Dependencies & Constraints *(mandatory)*

### Dependencies

**Frontend:**
- `better-auth` (npm package)
- Better Auth MCP plugin
- Next.js App Router (already installed)
- React hooks for auth state

**Backend:**
- `python-jose` (JWT encoding/decoding)
- `passlib` (password hashing - if not using Better Auth)
- `python-multipart` (form data parsing)
- FastAPI dependency injection for auth middleware

**Database:**
- Better Auth tables: `user`, `session`, `account`, `verification`
- Migration to add `user_id` to existing `todos` table

### Constraints

- **No OAuth**: Email/password authentication only
- **No Password Reset**: Out of scope for Phase II
- **No Email Verification**: Users can sign in immediately after registration
- **No MFA**: Single-factor authentication only
- **JWT Secret**: Must be 256-bit minimum (provided in requirements)
- **Stateless Backend**: Backend doesn't store sessions (JWT is self-contained)

## Out of Scope *(mandatory)*

The following capabilities are explicitly excluded from this feature:

- OAuth/SSO providers (Google, GitHub, etc.)
- Password reset/recovery flows
- Email verification before account activation
- Multi-factor authentication (MFA/2FA)
- Account deletion or deactivation
- Profile editing (change email, change password)
- "Remember me" checkbox (use Better Auth defaults)
- Session management UI (view active sessions, logout all devices)
- Rate limiting for brute force prevention (rely on Better Auth defaults)
- CAPTCHA integration
- Admin user roles or permissions
- Audit logs for authentication events

## Open Questions

**Q1:** Should existing todos (created before auth) be assigned to a default user or deleted?
**A:** Assign to first registered user OR delete (requires user decision before migration).

**Q2:** Should JWT be transmitted via cookie or Authorization header?
**A:** Authorization header (`Bearer <token>`) for API requests, Better Auth handles session cookie for page requests.

**Q3:** Should we implement refresh tokens or rely on 7-day expiration?
**A:** Use Better Auth default (7-day expiration, no explicit refresh token flow for Phase II).

---

**References:**
- Constitution: `.specify/memory/constitution.md` v1.1.0 Section VIII
- Better Auth Docs: https://www.better-auth.com/
- Better Auth MCP Plugin: https://www.better-auth.com/docs/plugins/mcp
