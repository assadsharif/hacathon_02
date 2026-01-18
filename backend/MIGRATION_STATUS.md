# Database Migration Status
**[Task]: AUTH-D1**
**Date**: 2026-01-12

## Migration Overview

Adding `user_id` column to `todos` table for user-scoped data.

## Migration Approaches

### Approach 1: SQLModel Auto-Creation (Development - RECOMMENDED)

For development, SQLModel's `create_all()` automatically creates/updates tables based on models.

**Status**: ✅ READY
**Models configured**:
- ✅ `models/user.py` - User table with UUID primary key
- ✅ `models/todo.py` - Todo table with user_id foreign key (Optional[str])
- ✅ `main.py` - Imports both models and calls `create_db_and_tables()`

**To apply migration**:
```bash
cd backend
# Install dependencies if not already installed
pip install -r requirements.txt

# Start FastAPI server - it will auto-create/update tables
uvicorn main:app --reload
```

**What happens**:
1. Server starts and runs `lifespan` function
2. Calls `create_db_and_tables()`
3. SQLModel inspects User and Todo models
4. Creates `users` table if not exists
5. Adds `user_id` column to `todos` table if not exists
6. Creates foreign key constraint and index

**Note**: Existing todos will have `user_id=NULL` initially. They won't be accessible via authenticated endpoints (which filter by user_id).

### Approach 2: Manual SQL Migration (Production)

For production or explicit control, run the migration SQL manually.

**Migration file**: `migrations/001_add_user_id_to_todos.sql`

**Options**:
1. **Via psql**:
   ```bash
   psql 'postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
   \i migrations/001_add_user_id_to_todos.sql
   ```

2. **Via Neon Console**:
   - Go to https://console.neon.tech
   - Open SQL Editor
   - Copy/paste migration SQL
   - Choose migration strategy (A, B, or C)
   - Execute

3. **Via Python script** (requires dependencies):
   ```bash
   python run_migration.py
   ```

## Environment Configuration

**✅ Configured**:
- `backend/.env` - Contains `DATABASE_URL` and `JWT_SECRET`
- `frontend/.env.local` - Contains `DATABASE_URL`, `JWT_SECRET`, and app URLs

## Verification Steps

After migration, verify:

```sql
-- Check user_id column exists
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'todos' AND column_name = 'user_id';

-- Check index exists
SELECT indexname FROM pg_indexes
WHERE tablename = 'todos' AND indexname = 'idx_todos_user_id';

-- Check foreign key constraint
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'todos' AND constraint_type = 'FOREIGN KEY';
```

## Next Steps

1. ✅ Environment variables configured
2. ⚠️  Install Python dependencies (manual step required)
3. ⏳ Start backend server (SQLModel auto-migration)
4. ⏳ Verify tables created (users, todos with user_id)
5. ⏳ Test user registration
6. ⏳ Test authenticated todo operations

## Migration Decision

**For AUTH-D1 testing, we will use Approach 1 (SQLModel Auto-Creation)**:
- Faster for development
- No manual SQL execution needed
- Tables auto-created on server start
- Existing todos will be orphaned (user_id=NULL) but new todos will work correctly

---

## Manual Steps Required

**⚠️  Python dependencies not installed**

Before starting the server, install backend dependencies:

```bash
# Option 1: Install pip if not available
sudo apt update
sudo apt install python3-pip

# Option 2: Create virtual environment (recommended)
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```

**Status**: ⏳ WAITING FOR DEPENDENCY INSTALLATION
**After installation, run**: `cd backend && uvicorn main:app --reload`
