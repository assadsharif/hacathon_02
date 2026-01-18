# Database Migrations

**[Task]: AUTH-A3**
**[From]: authentication.spec.md, plan.md**

This directory contains SQL migration scripts for Phase II database schema changes.

## Migration Files

| File | Description | Status |
|------|-------------|--------|
| `001_add_user_id_to_todos.sql` | Add user_id foreign key to todos table | Ready to apply |

## How to Apply Migrations

### Option 1: SQLModel Auto-Creation (Development)

For development, SQLModel can auto-create tables based on models:

```bash
# Start the FastAPI server - it will create/update tables automatically
cd backend
uvicorn main:app --reload
```

**Note**: SQLModel's `create_all()` will add new columns but won't handle data migration strategies.

### Option 2: Manual Migration (Production)

For production or when you need control over data migration:

```bash
# Connect to Neon database
psql 'postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'

# Run migration
\i migrations/001_add_user_id_to_todos.sql
```

### Option 3: Using Neon Console

1. Log in to Neon Console: https://console.neon.tech
2. Navigate to your project
3. Open SQL Editor
4. Copy and paste migration SQL
5. Execute

## Migration 001: Add user_id to todos

**Purpose**: Enable user-scoped todos for authentication

**Before running**:
1. Decide migration strategy for existing todos (see SQL file comments)
2. Uncomment ONE strategy in the SQL file
3. Apply the migration

**Migration Strategies**:

**Strategy A: Assign to First User** (Recommended for dev with test data)
- Existing todos assigned to first registered user
- Preserves data

**Strategy B: Delete Existing Todos** (Recommended for empty database)
- Cleans all existing todos
- Fresh start

**Strategy C: Create Migration User** (Recommended for production with data)
- Creates special "migration@system.local" account
- Existing todos assigned to migration user

**After migration**:
- All new todos MUST have user_id
- Todos filtered by user_id in all queries
- Data isolation enforced at database level

## Verification

After applying migration, verify:

```sql
-- Check column exists
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

-- Verify all todos have user_id (after making it NOT NULL)
SELECT COUNT(*) as todos_without_user
FROM todos
WHERE user_id IS NULL;
-- Should return 0
```

## Rollback

To rollback migration 001:

```sql
DROP INDEX IF EXISTS idx_todos_user_id;
ALTER TABLE todos DROP COLUMN IF EXISTS user_id;
```

## Future Migrations

When creating new migrations:

1. Use sequential numbering: `00X_description.sql`
2. Include [Task] reference in comments
3. Document migration strategies if applicable
4. Provide rollback instructions
5. Add verification queries
6. Update this README

## Important Notes

- **Never modify applied migrations** - create new ones instead
- **Test migrations on development database first**
- **Backup production data before applying migrations**
- **Coordinate migrations with application deployments**

---

**Constitution Reference**: `.specify/memory/constitution.md` v1.1.0 Section VIII
**Spec Reference**: `specs/phase-ii/authentication.spec.md`
**Plan Reference**: `specs/phase-ii/plan.md` - Database Schema Changes
