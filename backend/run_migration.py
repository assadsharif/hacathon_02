"""
Database Migration Runner
[Task]: AUTH-D1

This script runs the database migration to add user_id to the todos table.
It uses Strategy B (Delete existing todos) for a clean start.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

print("🔧 Connecting to Neon database...")
engine = create_engine(DATABASE_URL)

# Migration SQL with Strategy B (Delete existing todos)
migration_sql = """
-- ============================================================================
-- Migration: Add user_id column to todos table
-- ============================================================================

-- Step 1: Add user_id column (nullable initially)
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE CASCADE;

-- Step 2: Create index on user_id for query performance
CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos(user_id);

-- Strategy B: Delete all existing todos (fresh start for development)
DELETE FROM todos WHERE user_id IS NULL;

-- Step 3: Make user_id NOT NULL (all todos must have an owner)
ALTER TABLE todos
ALTER COLUMN user_id SET NOT NULL;

-- Add comment
COMMENT ON COLUMN todos.user_id IS 'Foreign key to users table (owner of todo)';
"""

print("📝 Running migration SQL...")
try:
    with engine.connect() as conn:
        # Execute migration
        conn.execute(text(migration_sql))
        conn.commit()
        print("✅ Migration completed successfully!")

        # Verify migration
        print("\n🔍 Verifying migration...")

        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'todos' AND column_name = 'user_id';
        """))
        column_info = result.fetchone()

        if column_info:
            print(f"  ✓ user_id column exists: {column_info[1]} (nullable: {column_info[2]})")
        else:
            print("  ✗ user_id column not found!")

        # Check if index exists
        result = conn.execute(text("""
            SELECT indexname FROM pg_indexes
            WHERE tablename = 'todos' AND indexname = 'idx_todos_user_id';
        """))
        index_info = result.fetchone()

        if index_info:
            print(f"  ✓ Index created: {index_info[0]}")
        else:
            print("  ✗ Index not found!")

        # Check foreign key constraint
        result = conn.execute(text("""
            SELECT constraint_name, constraint_type
            FROM information_schema.table_constraints
            WHERE table_name = 'todos' AND constraint_type = 'FOREIGN KEY';
        """))
        fk_info = result.fetchone()

        if fk_info:
            print(f"  ✓ Foreign key constraint: {fk_info[0]}")
        else:
            print("  ⚠ Foreign key constraint not found (may already exist)")

        # Count todos without user_id
        result = conn.execute(text("""
            SELECT COUNT(*) as todos_without_user
            FROM todos
            WHERE user_id IS NULL;
        """))
        count = result.fetchone()[0]
        print(f"  ✓ Todos without user_id: {count} (should be 0)")

        print("\n✅ Migration verification complete!")

except Exception as e:
    print(f"❌ Migration failed: {e}")
    raise

print("\n📊 Next steps:")
print("  1. Start the backend server: cd backend && uvicorn main:app --reload")
print("  2. Users table will be auto-created by SQLModel on first run")
print("  3. Register a new user to test authentication")
