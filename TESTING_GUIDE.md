# Authentication Testing Guide
**[Task]: AUTH-D2 through AUTH-D7**
**Date**: 2026-01-12

This guide provides step-by-step instructions for testing the authentication system implementation.

## Prerequisites

Before testing, ensure:
1. ✅ Backend `.env` configured with `DATABASE_URL` and `JWT_SECRET`
2. ✅ Frontend `.env.local` configured with all required variables
3. ⏳ Backend dependencies installed (`pip install -r requirements.txt`)
4. ⏳ Frontend dependencies installed (`npm install`)
5. ⏳ Backend server running (`uvicorn main:app --reload`)
6. ⏳ Frontend server running (`npm run dev`)

---

## AUTH-D2: Test User Registration Flow

**User Story**: As a new user, I want to create an account with email and password.

**Acceptance Criteria**:
- [FR-AUTH-001] User can register with email and password
- [FR-AUTH-002] Password is hashed before storage
- [FR-AUTH-003] User receives JWT token after registration

### Test Procedure

#### 1. Start Servers

**Terminal 1 - Backend**:
```bash
cd backend
# If using venv: source venv/bin/activate
uvicorn main:app --reload
```

Expected output:
```
🚀 Starting FastAPI server...
📊 Creating database tables...
✅ Database tables created successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

Expected output:
```
  ▲ Next.js 16.1.1
  - Local:        http://localhost:3000
```

#### 2. Test Sign-Up Page

1. **Navigate to sign-up page**:
   - Open browser: http://localhost:3000/sign-up

2. **Verify page renders**:
   - ✓ Page title: "Create your account"
   - ✓ Name input field
   - ✓ Email input field
   - ✓ Password input field (min 8 characters)
   - ✓ "Create account" button
   - ✓ Link to sign-in page

3. **Test validation**:
   - Try submitting with empty fields → Should show browser validation
   - Try password < 8 characters → Should show browser validation

4. **Create test user**:
   ```
   Name: Test User
   Email: test@example.com
   Password: password123
   ```

   Click "Create account"

5. **Expected behavior**:
   - ✓ Button shows "Creating account..." during request
   - ✓ Request sent to `/api/auth/sign-up`
   - ✓ Better Auth creates user in database
   - ✓ JWT token issued automatically
   - ✓ Redirect to home page (`/`)
   - ✓ User is signed in (session established)

6. **Verify in database** (optional):
   ```sql
   SELECT id, email, name, created_at FROM users WHERE email = 'test@example.com';
   ```
   - ✓ User record exists
   - ✓ Password is hashed (not plaintext)
   - ✓ `created_at` timestamp set

#### 3. Test Error Handling

1. **Duplicate email**:
   - Try registering again with `test@example.com`
   - Expected: Error message "Email already exists" or similar

2. **Invalid email format**:
   - Try: `notanemail`
   - Expected: Browser validation or error message

3. **Network error simulation**:
   - Stop backend server
   - Try to register
   - Expected: Error message "An unexpected error occurred"

### Test Results

**Status**: ⏳ PENDING
**Date**: ___________
**Tester**: ___________

- [ ] Sign-up page renders correctly
- [ ] Form validation works
- [ ] User can register successfully
- [ ] JWT token issued
- [ ] Redirect to home page works
- [ ] Error handling works

**Notes**: ___________

---

## AUTH-D3: Test Sign-In Flow

**User Story**: As a registered user, I want to sign in with my email and password.

**Acceptance Criteria**:
- [FR-AUTH-004] User can sign in with valid credentials
- [FR-AUTH-005] Invalid credentials are rejected
- [FR-AUTH-006] JWT token issued on successful sign-in

### Test Procedure

#### 1. Test Sign-In Page

1. **Sign out** (if signed in):
   - Click "Sign out" button on home page
   - OR navigate to: http://localhost:3000/sign-in

2. **Verify page renders**:
   - ✓ Page title: "Sign in to your account"
   - ✓ Email input field
   - ✓ Password input field
   - ✓ "Sign in" button
   - ✓ Link to sign-up page

#### 2. Test Valid Credentials

1. **Sign in with test user**:
   ```
   Email: test@example.com
   Password: password123
   ```

   Click "Sign in"

2. **Expected behavior**:
   - ✓ Button shows "Signing in..." during request
   - ✓ Request sent to `/api/auth/sign-in/email`
   - ✓ Better Auth verifies credentials
   - ✓ JWT token issued
   - ✓ Redirect to home page (`/`)
   - ✓ User is signed in

3. **Verify session**:
   - Check browser DevTools → Application → Cookies
   - ✓ Cookie: `better-auth.session_token` exists
   - ✓ Cookie is HttpOnly and Secure

#### 3. Test Invalid Credentials

1. **Wrong password**:
   ```
   Email: test@example.com
   Password: wrongpassword
   ```
   - Expected: Error message "Invalid email or password"

2. **Non-existent email**:
   ```
   Email: nonexistent@example.com
   Password: password123
   ```
   - Expected: Error message "Invalid email or password"

3. **Empty fields**:
   - Try submitting with empty email or password
   - Expected: Browser validation

#### 4. Test Session Persistence

1. **Sign in successfully**
2. **Refresh the page**
   - Expected: Still signed in (no redirect to sign-in page)
3. **Close browser and reopen**
   - Expected: Still signed in (session persists for 7 days)

### Test Results

**Status**: ⏳ PENDING
**Date**: ___________
**Tester**: ___________

- [ ] Sign-in page renders correctly
- [ ] Valid credentials work
- [ ] JWT token issued
- [ ] Redirect to home page works
- [ ] Invalid credentials rejected
- [ ] Error messages displayed
- [ ] Session persists across page refreshes

**Notes**: ___________

---

## AUTH-D4: Test Data Isolation

**User Story**: As a user, I want to see only my own todos, not other users' todos.

**Acceptance Criteria**:
- [FR-AUTH-010] All todo operations filtered by authenticated user
- [FR-AUTH-011] Users cannot access other users' todos

### Test Procedure

#### 1. Create Two Test Users

**User 1**:
1. Sign up: `user1@example.com` / `password123`
2. Create todos:
   - "User 1 Todo #1"
   - "User 1 Todo #2"
3. Sign out

**User 2**:
1. Sign up: `user2@example.com` / `password123`
2. Create todos:
   - "User 2 Todo #1"
   - "User 2 Todo #2"
3. Stay signed in

#### 2. Test Data Isolation

1. **As User 2, verify todos**:
   - Navigate to home page
   - Expected: See only User 2's todos (2 todos)
   - ✓ "User 2 Todo #1" visible
   - ✓ "User 2 Todo #2" visible
   - ✗ User 1's todos NOT visible

2. **Sign out and sign in as User 1**:
   - Sign out
   - Sign in with `user1@example.com`
   - Expected: See only User 1's todos (2 todos)
   - ✓ "User 1 Todo #1" visible
   - ✓ "User 1 Todo #2" visible
   - ✗ User 2's todos NOT visible

#### 3. Test API-Level Isolation

**Using browser DevTools or curl**:

1. **Get User 1's JWT token**:
   - Sign in as User 1
   - Open DevTools → Application → Cookies
   - Copy `better-auth.session_token` value

2. **Test LIST endpoint**:
   ```bash
   curl -H "Authorization: Bearer <user1_token>" \
        http://localhost:8000/api/todos
   ```
   - Expected: Returns only User 1's todos

3. **Test GET endpoint with User 2's todo ID**:
   ```bash
   # Try to access User 2's todo (ID from database)
   curl -H "Authorization: Bearer <user1_token>" \
        http://localhost:8000/api/todos/<user2_todo_id>
   ```
   - Expected: 404 Not Found (data isolation enforced)

4. **Test UPDATE endpoint**:
   ```bash
   curl -X PUT \
        -H "Authorization: Bearer <user1_token>" \
        -H "Content-Type: application/json" \
        -d '{"title":"Hacked!"}' \
        http://localhost:8000/api/todos/<user2_todo_id>
   ```
   - Expected: 404 Not Found

5. **Test DELETE endpoint**:
   ```bash
   curl -X DELETE \
        -H "Authorization: Bearer <user1_token>" \
        http://localhost:8000/api/todos/<user2_todo_id>
   ```
   - Expected: 404 Not Found

#### 4. Verify Database

```sql
-- Check todos are associated with correct users
SELECT t.id, t.title, t.user_id, u.email
FROM todos t
JOIN users u ON t.user_id = u.id
ORDER BY u.email, t.created_at;
```

Expected:
- User 1's todos have `user_id` matching User 1's UUID
- User 2's todos have `user_id` matching User 2's UUID

### Test Results

**Status**: ⏳ PENDING
**Date**: ___________
**Tester**: ___________

- [ ] User 1 sees only their todos
- [ ] User 2 sees only their todos
- [ ] API prevents cross-user access (GET)
- [ ] API prevents cross-user access (UPDATE)
- [ ] API prevents cross-user access (DELETE)
- [ ] Database correctly associates todos with users

**Notes**: ___________

---

## AUTH-D5: Test Unauthenticated Access Prevention

**User Story**: As the system, I want to prevent unauthenticated access to protected routes.

**Acceptance Criteria**:
- [FR-AUTH-012] Unauthenticated users redirected to sign-in page
- [FR-AUTH-013] API returns 401 for requests without valid JWT

### Test Procedure

#### 1. Test Frontend Middleware

1. **Clear session**:
   - Open DevTools → Application → Cookies
   - Delete `better-auth.session_token` cookie
   - OR use incognito/private browsing window

2. **Try to access home page**:
   - Navigate to: http://localhost:3000/
   - Expected: Redirect to `/sign-in?redirect=/`

3. **Verify public routes still accessible**:
   - Navigate to: http://localhost:3000/sign-in
   - Expected: Page loads (no redirect)
   - Navigate to: http://localhost:3000/sign-up
   - Expected: Page loads (no redirect)

#### 2. Test Backend API Protection

1. **Test LIST endpoint without token**:
   ```bash
   curl http://localhost:8000/api/todos
   ```
   - Expected: 401 Unauthorized
   - Response: `{"detail":"Invalid token: ..."}`

2. **Test CREATE endpoint without token**:
   ```bash
   curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"title":"Test Todo"}' \
        http://localhost:8000/api/todos
   ```
   - Expected: 401 Unauthorized

3. **Test with invalid token**:
   ```bash
   curl -H "Authorization: Bearer invalid_token_here" \
        http://localhost:8000/api/todos
   ```
   - Expected: 401 Unauthorized
   - Response: `{"detail":"Invalid token: ..."}`

4. **Test with expired token**:
   - Use a JWT token generator to create an expired token
   - Try to access API
   - Expected: 401 Unauthorized

#### 3. Test Sign-In Required Flow

1. **Start unauthenticated**
2. **Try to access `/`**:
   - Redirect to `/sign-in?redirect=/`
3. **Sign in successfully**:
   - After sign-in, redirect back to `/` (original destination)

### Test Results

**Status**: ⏳ PENDING
**Date**: ___________
**Tester**: ___________

- [ ] Unauthenticated users cannot access home page
- [ ] Redirect to sign-in page works
- [ ] Public routes (sign-in, sign-up) accessible
- [ ] API returns 401 without token
- [ ] API returns 401 with invalid token
- [ ] Sign-in redirect flow works

**Notes**: ___________

---

## AUTH-D6: Update API Documentation

**Task**: Document authentication requirements in API documentation.

### Documentation Updates

Create `backend/docs/API.md` with:

1. **Authentication Overview**
   - JWT-based authentication
   - HS256 signing algorithm
   - Authorization header format: `Bearer <token>`

2. **Obtaining JWT Token**
   - POST `/api/auth/sign-up` - Register and get token
   - POST `/api/auth/sign-in/email` - Sign in and get token

3. **Protected Endpoints**
   - All `/api/todos/*` endpoints require authentication
   - Include example curl commands with Authorization header

4. **Error Responses**
   - 401 Unauthorized - Missing or invalid token
   - 404 Not Found - Resource not found or not owned by user

### Status

**Status**: ⏳ PENDING (see next section for content)

---

## AUTH-D7: Update Implementation Log

**Task**: Document all authentication implementation work.

### Log Entries to Add

Create `specs/phase-ii/IMPLEMENTATION_LOG.md` with:

1. **AUTH-A: Database Schema Changes**
   - AUTH-A1: Created User model
   - AUTH-A2: Added user_id to Todo model
   - AUTH-A3: Created database migration script

2. **AUTH-B: Backend JWT Verification**
   - AUTH-B1: Updated dependencies (python-jose, passlib)
   - AUTH-B2: Created JWT auth middleware
   - AUTH-B3: Updated all todo endpoints with authentication
   - AUTH-B4: Updated schemas with user_id
   - AUTH-B5: Added environment variable configuration

3. **AUTH-C: Frontend Better Auth Integration**
   - AUTH-C1: Installed Better Auth
   - AUTH-C2: Created Better Auth configuration
   - AUTH-C3: Created sign-up page
   - AUTH-C4: Created sign-in page
   - AUTH-C5: Updated API client with JWT
   - AUTH-C6: Created protected route middleware
   - AUTH-C7: Added sign-out button components
   - AUTH-C8: Added environment variables

4. **AUTH-D: Integration & Testing**
   - AUTH-D1: Database migration preparation
   - AUTH-D2-D5: Test procedures documented
   - AUTH-D6: API documentation
   - AUTH-D7: Implementation log (this file)

### Status

**Status**: ⏳ PENDING (see next section for content)

---

## Summary

**Total Test Cases**: 4 major flows + 2 documentation tasks

**Completion Checklist**:
- [ ] AUTH-D1: Database migration prepared ✅ (COMPLETED)
- [ ] AUTH-D2: User registration tested
- [ ] AUTH-D3: Sign-in flow tested
- [ ] AUTH-D4: Data isolation verified
- [ ] AUTH-D5: Unauthenticated access prevention tested
- [ ] AUTH-D6: API documentation updated
- [ ] AUTH-D7: Implementation log created

**Next Steps After Testing**:
1. Fix any issues found during testing
2. Update documentation with test results
3. Create demo video or screenshots
4. Prepare for production deployment
