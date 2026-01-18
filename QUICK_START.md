# Quick Start Guide
**Authentication-Enabled Todo Application**
**Date**: 2026-01-12

Welcome! This guide will help you start the application in under 5 minutes.

---

## ✅ Setup Complete!

All dependencies have been installed:
- ✅ Backend Python dependencies (FastAPI, SQLModel, python-jose)
- ✅ Frontend dependencies (Next.js, Better Auth)
- ✅ Environment variables configured
- ✅ Database migration ready

---

## 🚀 Starting the Application

You need **2 terminal windows** to run both servers.

### Terminal 1: Start Backend

```bash
./start-backend.sh
```

**Expected Output**:
```
🚀 Starting FastAPI server...
📊 Creating database tables...
✅ Database tables created successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**What it does**:
- Connects to Neon PostgreSQL database
- Auto-creates `users` and `todos` tables
- Starts FastAPI server on port 8000

**API Documentation**: http://127.0.0.1:8000/docs

---

### Terminal 2: Start Frontend

```bash
./start-frontend.sh
```

**Expected Output**:
```
  ▲ Next.js 16.1.1
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

**What it does**:
- Starts Next.js development server
- Enables Better Auth for authentication
- Serves the React application

**Application**: http://localhost:3000

---

## 📝 Testing the Application

### Step 1: Register a New User

1. Open browser: http://localhost:3000/sign-up
2. Enter your details:
   - Name: Your Name
   - Email: test@example.com
   - Password: password123 (min 8 characters)
3. Click "Create account"
4. You'll be auto-signed in and redirected to home page

### Step 2: Sign In

1. Open: http://localhost:3000/sign-in
2. Enter credentials
3. Click "Sign in"
4. Redirected to home page

### Step 3: Create Todos

1. On the home page, create some todos
2. All todos are automatically scoped to your user
3. Other users cannot see your todos

### Step 4: Test Data Isolation

1. Sign out
2. Create a second user: user2@example.com
3. Create todos for this user
4. Sign out and sign in as first user
5. Verify: You only see your own todos!

---

## 📚 Documentation

All documentation is available in the repository:

- **API Documentation**: `backend/docs/API.md`
  - All 5 endpoints with curl examples
  - Authentication guide
  - Error handling

- **Testing Guide**: `TESTING_GUIDE.md`
  - Complete test procedures
  - Manual testing steps
  - Data isolation verification

- **Implementation Log**: `specs/phase-ii/IMPLEMENTATION_LOG.md`
  - All 24 tasks completed
  - Architecture overview
  - Code references

- **Migration Status**: `backend/MIGRATION_STATUS.md`
  - Database migration details
  - Migration strategies

---

## 🔧 Troubleshooting

### Backend won't start

**Problem**: Database connection error

**Solution**: Check your `.env` file:
```bash
cat backend/.env
```

Ensure `DATABASE_URL` and `JWT_SECRET` are set.

---

### Frontend won't start

**Problem**: Dependencies missing

**Solution**: Reinstall:
```bash
cd frontend
npm install
```

---

### Can't sign up / sign in

**Problem**: Database tables not created

**Solution**:
1. Stop backend server (Ctrl+C)
2. Restart it: `./start-backend.sh`
3. Look for "✅ Database tables created successfully"

---

### JWT token errors

**Problem**: "Invalid token" errors

**Solution**: Ensure `JWT_SECRET` matches in both files:
- `backend/.env`
- `frontend/.env.local`

Both should have: `JWT_SECRET=93457b5f5d59fd9d65726648e22a4e28`

---

## 🎯 Key URLs

**Backend**:
- Server: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000

**Frontend**:
- Home: http://localhost:3000
- Sign Up: http://localhost:3000/sign-up
- Sign In: http://localhost:3000/sign-in

---

## 🔐 Authentication Flow

1. User signs up → Better Auth creates account in database
2. Better Auth issues JWT token
3. Token stored in HttpOnly cookie
4. Frontend middleware checks session on every route
5. API client attaches JWT to all backend requests
6. Backend verifies JWT and extracts user_id
7. All queries filtered by user_id

---

## 📊 Database Schema

**users** table:
- id (UUID)
- email (unique)
- password_hash
- name
- created_at

**todos** table:
- id (serial)
- user_id (UUID, foreign key)
- title
- description
- status (active/completed)
- created_at
- updated_at

---

## 🛠️ Manual Commands

If you prefer manual commands over scripts:

**Backend**:
```bash
cd backend
./venv/bin/uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
npm run dev
```

---

## 🔍 Viewing the Database

To see your data in the database:

```bash
# Install psql if needed
sudo apt install postgresql-client

# Connect to Neon database
psql 'postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

# List tables
\dt

# View users
SELECT id, email, name, created_at FROM users;

# View todos
SELECT t.id, t.title, t.status, u.email
FROM todos t
JOIN users u ON t.user_id = u.id;

# Exit
\q
```

---

## 🎨 What's Implemented

**Backend** (FastAPI):
- ✅ User model with UUID
- ✅ Todo model with user_id
- ✅ JWT authentication middleware
- ✅ 5 protected CRUD endpoints
- ✅ User-scoped data filtering
- ✅ Error handling (401, 404)

**Frontend** (Next.js):
- ✅ Better Auth integration
- ✅ Sign-up page
- ✅ Sign-in page
- ✅ Protected route middleware
- ✅ JWT-enabled API client
- ✅ Sign-out functionality

**Security**:
- ✅ JWT tokens (HS256)
- ✅ Password hashing (bcrypt)
- ✅ Data isolation (user-scoped)
- ✅ HttpOnly cookies
- ✅ API authentication required

---

## 📖 Next Steps

After testing:

1. **Follow Testing Guide**: Run all tests in `TESTING_GUIDE.md`
2. **Review API Documentation**: See all endpoints in `backend/docs/API.md`
3. **Read Implementation Log**: Understand architecture in `specs/phase-ii/IMPLEMENTATION_LOG.md`

---

## ❓ Need Help?

1. Check troubleshooting section above
2. Review documentation files
3. Check backend logs in Terminal 1
4. Check frontend logs in Terminal 2
5. Verify environment variables are set correctly

---

**Ready to start? Open 2 terminals and run the start scripts!** 🚀

```bash
# Terminal 1
./start-backend.sh

# Terminal 2
./start-frontend.sh
```

Then open http://localhost:3000 in your browser!
