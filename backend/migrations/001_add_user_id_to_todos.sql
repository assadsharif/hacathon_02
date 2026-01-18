-- [Task]: AUTH-A3
-- [From]: authentication.spec.md, plan.md Database Schema Changes
--
-- Migration: Add user_id column to todos table
-- Created: 2026-01-12
-- Purpose: Enable user-scoped todos for authentication feature
--
-- This migration adds a user_id foreign key to the todos table,
-- establishing a one-to-many relationship (User -> Todos).
--
-- IMPORTANT: Handle existing todos before running this migration.
-- See "Migration Strategies" section below.

-- ============================================================================
-- Step 1: Add user_id column to todos table
-- ============================================================================

ALTER TABLE todos
ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE CASCADE;

COMMENT ON COLUMN todos.user_id IS 'Foreign key to users table (owner of todo)';


-- ============================================================================
-- Step 2: Create index on user_id for query performance
-- ============================================================================

CREATE INDEX idx_todos_user_id ON todos(user_id);

COMMENT ON INDEX idx_todos_user_id IS 'Index for efficient user-scoped todo queries';


-- ============================================================================
-- Migration Strategies for Existing Todos
-- ============================================================================
--
-- Before running this migration, decide how to handle existing todos.
-- Uncomment ONE of the strategies below:

-- STRATEGY A: Assign existing todos to first registered user
-- ----------------------------------------------------------------------------
-- Pros: Preserves existing data
-- Cons: All existing todos will belong to one user
--
-- UPDATE todos
-- SET user_id = (SELECT id FROM users ORDER BY created_at ASC LIMIT 1)
-- WHERE user_id IS NULL;


-- STRATEGY B: Delete all existing todos (fresh start)
-- ----------------------------------------------------------------------------
-- Pros: Clean slate, no data ownership confusion
-- Cons: Loses existing data
--
-- DELETE FROM todos;


-- STRATEGY C: Create a "migration" default user
-- ----------------------------------------------------------------------------
-- Pros: Existing todos preserved under dedicated account
-- Cons: Requires creating a special user account
--
-- INSERT INTO users (id, email, password_hash, name, created_at)
-- VALUES (
--     gen_random_uuid(),
--     'migration@system.local',
--     '$2b$12$dummy_hash_for_migration_user',
--     'Migration User',
--     NOW()
-- );
--
-- UPDATE todos
-- SET user_id = (SELECT id FROM users WHERE email = 'migration@system.local')
-- WHERE user_id IS NULL;


-- ============================================================================
-- Step 3: Make user_id NOT NULL (after handling existing todos)
-- ============================================================================
--
-- After choosing a migration strategy above, make user_id required:

-- ALTER TABLE todos
-- ALTER COLUMN user_id SET NOT NULL;


-- ============================================================================
-- Rollback Instructions
-- ============================================================================
--
-- To rollback this migration:
--
-- DROP INDEX IF EXISTS idx_todos_user_id;
-- ALTER TABLE todos DROP COLUMN IF EXISTS user_id;


-- ============================================================================
-- Verification Queries
-- ============================================================================
--
-- Check if column was added:
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'todos' AND column_name = 'user_id';
--
-- Check if index was created:
-- SELECT indexname FROM pg_indexes WHERE tablename = 'todos';
--
-- Verify foreign key constraint:
-- SELECT constraint_name, constraint_type
-- FROM information_schema.table_constraints
-- WHERE table_name = 'todos' AND constraint_type = 'FOREIGN KEY';
