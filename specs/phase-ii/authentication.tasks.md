# Authentication Implementation Tasks

**Feature**: User Authentication with Better Auth + JWT
**Spec**: [authentication.spec.md](./authentication.spec.md)
**Plan**: [plan.md](./plan.md) - M5: Authentication & User-Scoped Data
**Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) v1.1.0 Section VIII

---

## Task Group AUTH-A: Database Schema & Migration

### AUTH-A1: Create User Model (Backend)
**[Task]: AUTH-A1**
**[From]: authentication.spec.md FR-AUTH-001, plan.md Database Schema**

**Description**: Create SQLModel User table for authentication

**Preconditions**:
- SQLModel installed
- Neon database connection configured

**Implementation**:
1. Create `backend/models/user.py`
2. Define User model with fields: id (UUID), email, password_hash, name, created_at
3. Add email unique constraint
4. Import into `backend/models/__init__.py`

**Acceptance Criteria**:
- User model has all required fields
- Email field has unique constraint
- ID uses UUID with auto-generation
- Model registered with SQLModel

**Expected Outputs**:
- `backend/models/user.py` created
- User model importable from `backend.models`

---

### AUTH-A2: Add user_id to Todo Model
**[Task]: AUTH-A2**
**[From]: authentication.spec.md FR-AUTH-014, plan.md Database Schema**

**Description**: Add user_id foreign key to existing Todo model

**Preconditions**:
- AUTH-A1 completed
- Todo model exists in `backend/models.py`

**Implementation**:
1. Add `user_id: Optional[str]` field to Todo model
2. Add Field with foreign key constraint: `Field(foreign_key="users.id")`
3. Update model docstring to mention user association
4. Update Config example to include user_id

**Acceptance Criteria**:
- Todo model has user_id field
- Foreign key references users.id
- Field is Optional (for migration compatibility)

**Expected Outputs**:
- `backend/models.py` updated with user_id field

---

### AUTH-A3: Create Database Migration Script
**[Task]: AUTH-A3**
**[From]: plan.md Database Schema Changes**

**Description**: Create SQL migration to add user_id column to todos table

**Preconditions**:
- AUTH-A1 and AUTH-A2 completed

**Implementation**:
1. Create `backend/migrations/001_add_user_id_to_todos.sql`
2. Add ALTER TABLE statement to add user_id column
3. Add CREATE INDEX statement for user_id
4. Add comments explaining migration strategy options
5. Document in migration README

**Acceptance Criteria**:
- Migration SQL file created
- Includes ALTER TABLE and CREATE INDEX
- Documents handling of existing todos

**Expected Outputs**:
- `backend/migrations/001_add_user_id_to_todos.sql`
- Migration instructions in comments

---

## Task Group AUTH-B: Backend JWT Verification

### AUTH-B1: Install JWT Dependencies
**[Task]: AUTH-B1**
**[From]: plan.md Backend Implementation**

**Description**: Add python-jose for JWT handling

**Preconditions**:
- Backend requirements.txt exists

**Implementation**:
1. Add `python-jose[cryptography]==3.3.0` to requirements.txt
2. Add `passlib[bcrypt]==1.7.4` for password hashing (if needed)
3. Run `pip install -r requirements.txt`

**Acceptance Criteria**:
- python-jose installed
- Can import jose.jwt

**Expected Outputs**:
- `backend/requirements.txt` updated

---

### AUTH-B2: Create JWT Auth Middleware
**[Task]: AUTH-B2**
**[From]: authentication.spec.md FR-AUTH-009, plan.md JWT Verification Middleware**

**Description**: Create FastAPI dependency for JWT verification

**Preconditions**:
- AUTH-B1 completed
- JWT_SECRET in .env

**Implementation**:
1. Create `backend/auth.py`
2. Implement `get_current_user_id()` dependency
3. Extract Authorization header
4. Verify JWT signature with python-jose
5. Extract user_id from claims
6. Raise HTTPException(401) for invalid tokens

**Acceptance Criteria**:
- Function verifies JWT signature
- Returns user_id from valid tokens
- Raises 401 for invalid/expired tokens
- Uses environment variable for secret

**Expected Outputs**:
- `backend/auth.py` with `get_current_user_id()` function

---

### AUTH-B3: Update Todo Endpoints with Auth
**[Task]: AUTH-B3**
**[From]: authentication.spec.md FR-AUTH-011, FR-AUTH-013, plan.md Updated API Endpoints**

**Description**: Add user_id filtering to all todo CRUD endpoints

**Preconditions**:
- AUTH-B2 completed
- Todo endpoints exist

**Implementation**:
1. Import `get_current_user_id` in `backend/routers/todos.py`
2. Add `user_id: str = Depends(get_current_user_id)` to each endpoint
3. Update GET /api/todos: filter by user_id
4. Update GET /api/todos/{id}: filter by user_id, return 404 if not owned
5. Update POST /api/todos: set user_id on new todo
6. Update PUT /api/todos/{id}: filter by user_id before update
7. Update DELETE /api/todos/{id}: filter by user_id before delete

**Acceptance Criteria**:
- All endpoints require JWT
- All queries filter by user_id
- Users cannot access other users' todos (404 response)
- New todos automatically associated with current user

**Expected Outputs**:
- `backend/routers/todos.py` updated with auth

---

### AUTH-B4: Update Todo Schemas with user_id
**[Task]: AUTH-B4**
**[From]: authentication.spec.md Key Entities**

**Description**: Add user_id to Pydantic schemas

**Preconditions**:
- AUTH-A2 completed

**Implementation**:
1. Add `user_id: str` to TodoResponse schema
2. Do NOT add user_id to TodoCreate (auto-assigned from JWT)
3. Do NOT add user_id to TodoUpdate (cannot change owner)
4. Update schema docstrings

**Acceptance Criteria**:
- TodoResponse includes user_id
- TodoCreate does NOT include user_id
- TodoUpdate does NOT include user_id

**Expected Outputs**:
- `backend/schemas.py` updated

---

### AUTH-B5: Add Environment Variable Configuration
**[Task]: AUTH-B5**
**[From]: plan.md Environment Variables**

**Description**: Add JWT_SECRET to backend environment

**Preconditions**:
- None

**Implementation**:
1. Add `JWT_SECRET` to `backend/.env`
2. Set value: `93457b5f5d59fd9d65726648e22a4e28`
3. Add `JWT_SECRET=your-secret-key-here` to `backend/.env.example`
4. Update `backend/auth.py` to read from env

**Acceptance Criteria**:
- JWT_SECRET in .env
- .env.example documents it
- auth.py reads from environment

**Expected Outputs**:
- `backend/.env` updated
- `backend/.env.example` updated

---

## Task Group AUTH-C: Frontend Better Auth Integration

### AUTH-C1: Install Better Auth Dependencies
**[Task]: AUTH-C1**
**[From]: plan.md Frontend Implementation**

**Description**: Install better-auth npm package

**Preconditions**:
- Frontend package.json exists

**Implementation**:
1. Run `npm install better-auth`
2. Verify installation

**Acceptance Criteria**:
- better-auth in package.json dependencies
- Can import from 'better-auth'

**Expected Outputs**:
- `frontend/package.json` updated

---

### AUTH-C2: Create Better Auth Configuration
**[Task]: AUTH-C2**
**[From]: authentication.spec.md FR-AUTH-015-020, plan.md Better Auth Configuration**

**Description**: Set up Better Auth client with MCP plugin

**Preconditions**:
- AUTH-C1 completed

**Implementation**:
1. Create `frontend/lib/auth.ts`
2. Import betterAuth and mcp plugin
3. Configure with loginPage: "/sign-in"
4. Configure JWT with secret from env
5. Set expiresIn: "7d"
6. Export auth instance

**Acceptance Criteria**:
- Better Auth configured
- MCP plugin enabled
- JWT settings configured
- Reads secret from environment

**Expected Outputs**:
- `frontend/lib/auth.ts` created

---

### AUTH-C3: Create Sign-Up Page
**[Task]: AUTH-C3**
**[From]: authentication.spec.md User Story 1, FR-AUTH-015**

**Description**: Create user registration page

**Preconditions**:
- AUTH-C2 completed

**Implementation**:
1. Create `frontend/app/sign-up/page.tsx`
2. Add form with email and password fields
3. Add password confirmation field
4. Add validation (email format, min 8 chars)
5. Call Better Auth registration
6. Handle errors and display messages
7. Redirect to /sign-in on success

**Acceptance Criteria**:
- Form accepts email and password
- Validates input client-side
- Calls Better Auth registration
- Shows error messages
- Redirects to sign-in on success

**Expected Outputs**:
- `frontend/app/sign-up/page.tsx` created

---

### AUTH-C4: Create Sign-In Page
**[Task]: AUTH-C4**
**[From]: authentication.spec.md User Story 2, FR-AUTH-016**

**Description**: Create user sign-in page

**Preconditions**:
- AUTH-C2 completed

**Implementation**:
1. Create `frontend/app/sign-in/page.tsx`
2. Add form with email and password fields
3. Call Better Auth sign-in
4. Handle errors (invalid credentials)
5. Store JWT token in Better Auth session
6. Redirect to /todos on success

**Acceptance Criteria**:
- Form accepts credentials
- Calls Better Auth sign-in
- Handles authentication errors
- Stores JWT on success
- Redirects to /todos

**Expected Outputs**:
- `frontend/app/sign-in/page.tsx` created

---

### AUTH-C5: Update API Client with JWT
**[Task]: AUTH-C5**
**[From]: authentication.spec.md FR-AUTH-018, plan.md API Client Enhancement**

**Description**: Modify TodoApi to attach JWT to requests

**Preconditions**:
- AUTH-C2 completed
- API client exists (lib/api.ts)

**Implementation**:
1. Add `getAuthHeader()` method to TodoApi class
2. Read JWT from Better Auth session
3. Return `Bearer ${token}` format
4. Update all API methods to include Authorization header
5. Handle 401 responses by redirecting to /sign-in

**Acceptance Criteria**:
- All API requests include Authorization header
- JWT read from Better Auth session
- 401 responses trigger redirect to sign-in

**Expected Outputs**:
- `frontend/lib/api.ts` updated

---

### AUTH-C6: Create Protected Route Middleware
**[Task]: AUTH-C6**
**[From]: authentication.spec.md FR-AUTH-019, FR-AUTH-020**

**Description**: Add middleware to protect /todos routes

**Preconditions**:
- AUTH-C2 completed

**Implementation**:
1. Create `frontend/middleware.ts`
2. Check Better Auth session
3. Redirect to /sign-in if no session
4. Allow access if authenticated
5. Configure matcher for protected routes

**Acceptance Criteria**:
- Unauthenticated users redirected to /sign-in
- Authenticated users can access /todos
- Middleware runs on /todos* paths

**Expected Outputs**:
- `frontend/middleware.ts` created

---

### AUTH-C7: Add Sign-Out Button
**[Task]: AUTH-C7**
**[From]: authentication.spec.md User Story 4**

**Description**: Add sign-out functionality to UI

**Preconditions**:
- AUTH-C2 completed
- Layout component exists

**Implementation**:
1. Update `frontend/app/layout.tsx`
2. Add sign-out button in header
3. Call Better Auth signOut()
4. Clear session and JWT
5. Redirect to /sign-in

**Acceptance Criteria**:
- Sign-out button visible when authenticated
- Clears session on click
- Redirects to sign-in

**Expected Outputs**:
- `frontend/app/layout.tsx` updated

---

### AUTH-C8: Add Environment Variables (Frontend)
**[Task]: AUTH-C8**
**[From]: plan.md Environment Variables**

**Description**: Configure frontend environment for Better Auth

**Preconditions**:
- None

**Implementation**:
1. Add to `frontend/.env.local`:
   - `BETTER_AUTH_SECRET=93457b5f5d59fd9d65726648e22a4e28`
   - `BETTER_AUTH_URL=http://localhost:3000`
2. Update `.env.local.example`

**Acceptance Criteria**:
- BETTER_AUTH_SECRET in .env.local
- BETTER_AUTH_URL configured
- Example file updated

**Expected Outputs**:
- `frontend/.env.local` updated

---

## Task Group AUTH-D: Integration & Testing

### AUTH-D1: Run Database Migration
**[Task]: AUTH-D1**
**[From]: AUTH-A3**

**Description**: Apply database migration for user_id column

**Preconditions**:
- AUTH-A3 migration script created
- Neon database accessible

**Implementation**:
1. Connect to Neon database
2. Execute migration SQL
3. Verify user_id column added
4. Verify index created

**Acceptance Criteria**:
- Migration executed successfully
- todos table has user_id column
- Index on user_id exists

**Expected Outputs**:
- Database schema updated

---

### AUTH-D2: Test User Registration Flow
**[Task]: AUTH-D2**
**[From]: authentication.spec.md User Story 1**

**Description**: Manual test of registration

**Preconditions**:
- AUTH-C3 completed
- Backend running
- Frontend running

**Implementation**:
1. Navigate to /sign-up
2. Submit email and password
3. Verify user created in database
4. Verify password is hashed
5. Verify redirect to /sign-in

**Acceptance Criteria**:
- Can register new user
- Password hashed in database
- Redirects to sign-in

**Expected Outputs**:
- Test passed confirmation

---

### AUTH-D3: Test Sign-In Flow
**[Task]: AUTH-D3**
**[From]: authentication.spec.md User Story 2**

**Description**: Manual test of sign-in

**Preconditions**:
- AUTH-D2 completed
- User registered

**Implementation**:
1. Navigate to /sign-in
2. Submit correct credentials
3. Verify JWT token issued
4. Verify redirect to /todos
5. Verify can make authenticated API requests

**Acceptance Criteria**:
- Can sign in with valid credentials
- JWT token stored
- Redirects to /todos
- API requests authenticated

**Expected Outputs**:
- Test passed confirmation

---

### AUTH-D4: Test Data Isolation
**[Task]: AUTH-D4**
**[From]: authentication.spec.md User Story 3, Acceptance Scenarios**

**Description**: Verify users only see their own todos

**Preconditions**:
- AUTH-D3 completed

**Implementation**:
1. Create User A, sign in, create 3 todos
2. Sign out
3. Create User B, sign in, create 2 todos
4. Verify User B sees only 2 todos
5. Sign out, sign in as User A
6. Verify User A sees only 3 original todos
7. Try to access User B's todo by ID (should get 404)

**Acceptance Criteria**:
- User A sees only their todos
- User B sees only their todos
- Cross-user access returns 404
- No data leakage between users

**Expected Outputs**:
- Data isolation verified

---

### AUTH-D5: Test Unauthenticated Access Prevention
**[Task]: AUTH-D5**
**[From]: authentication.spec.md User Story 5**

**Description**: Verify unauthenticated requests are blocked

**Preconditions**:
- All auth components implemented

**Implementation**:
1. Make API request without JWT → expect 401
2. Try to access /todos without session → expect redirect
3. Use expired JWT → expect 401
4. Use invalid JWT → expect 401

**Acceptance Criteria**:
- All unauthorized requests return 401
- Protected pages redirect to sign-in
- Invalid/expired tokens rejected

**Expected Outputs**:
- Security test passed

---

### AUTH-D6: Update API Documentation
**[Task]: AUTH-D6**
**[From]: authentication.spec.md**

**Description**: Document authentication in API reference

**Preconditions**:
- All auth tasks completed

**Implementation**:
1. Update `backend/API_REFERENCE.md`
2. Add Authentication section
3. Document Authorization header requirement
4. Document 401 error responses
5. Add registration/sign-in examples

**Acceptance Criteria**:
- API docs include auth information
- Examples show JWT usage
- Error responses documented

**Expected Outputs**:
- `backend/API_REFERENCE.md` updated

---

### AUTH-D7: Update Implementation Log
**[Task]: AUTH-D7**
**[From]: SDD workflow**

**Description**: Document authentication implementation in implement.md

**Preconditions**:
- All AUTH tasks completed

**Implementation**:
1. Update `specs/phase-ii/implement.md`
2. Mark M5 authentication tasks as complete
3. List all files changed
4. Document test results

**Acceptance Criteria**:
- Implementation log updated
- M5 marked complete
- All deliverables listed

**Expected Outputs**:
- `specs/phase-ii/implement.md` updated

---

## Task Execution Order

**Recommended sequence:**

1. **Database Layer** (AUTH-A1 → AUTH-A2 → AUTH-A3)
2. **Backend Auth** (AUTH-B1 → AUTH-B2 → AUTH-B3 → AUTH-B4 → AUTH-B5)
3. **Frontend Auth** (AUTH-C1 → AUTH-C2 → AUTH-C3 → AUTH-C4 → AUTH-C5 → AUTH-C6 → AUTH-C7 → AUTH-C8)
4. **Integration** (AUTH-D1 → AUTH-D2 → AUTH-D3 → AUTH-D4 → AUTH-D5 → AUTH-D6 → AUTH-D7)

**Dependencies:**
- AUTH-B depends on AUTH-A (database schema)
- AUTH-C depends on AUTH-B (backend endpoints)
- AUTH-D depends on AUTH-A, AUTH-B, AUTH-C (integration testing)

**Time Estimate:** ~4-6 hours for full implementation

---

## Task Discipline Reminders

- One task at a time (no parallelization without approval)
- Reference spec/plan/task in all commits
- Run tests after each task group
- Update implement.md with progress
- No scope expansion beyond task definition

**Constitution Reference**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) v1.1.0
**Spec Reference**: [authentication.spec.md](./authentication.spec.md)
**Plan Reference**: [plan.md](./plan.md) - M5: Authentication & User-Scoped Data
