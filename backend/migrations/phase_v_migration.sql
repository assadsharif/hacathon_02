-- [Task]: T006
-- Phase V Migration: Add advanced task features and event-driven entities
-- Run this migration against PostgreSQL database
-- Reference: specs/005-phase-v-event-driven/data-model.md

BEGIN;

-- ============================================================================
-- STEP 1: Add new columns to todos table
-- ============================================================================

-- Add priority column (low, medium, high)
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';

-- Add due_date for task deadlines
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;

-- Add reminder_at for scheduled reminders
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS reminder_at TIMESTAMP;

-- Add recurrence fields for recurring tasks
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS recurrence_rule VARCHAR(20);

ALTER TABLE todos
ADD COLUMN IF NOT EXISTS recurrence_interval INT DEFAULT 1;

ALTER TABLE todos
ADD COLUMN IF NOT EXISTS recurrence_end_date TIMESTAMP;

-- Add parent_task_id for recurring task instances
ALTER TABLE todos
ADD COLUMN IF NOT EXISTS parent_task_id INT REFERENCES todos(id) ON DELETE SET NULL;

-- ============================================================================
-- STEP 2: Create tags table
-- ============================================================================

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(name, user_id)
);

-- ============================================================================
-- STEP 3: Create todo_tags junction table (many-to-many)
-- ============================================================================

CREATE TABLE IF NOT EXISTS todo_tags (
    todo_id INT NOT NULL REFERENCES todos(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (todo_id, tag_id)
);

-- ============================================================================
-- STEP 4: Create task_events table for audit log (immutable)
-- ============================================================================

CREATE TABLE IF NOT EXISTS task_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id INT NOT NULL,
    user_id UUID NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- STEP 5: Create indexes for performance
-- ============================================================================

-- Index for todos due_date queries (reminders)
CREATE INDEX IF NOT EXISTS idx_todos_due_date
ON todos(due_date)
WHERE due_date IS NOT NULL;

-- Index for recurring task parent lookup
CREATE INDEX IF NOT EXISTS idx_todos_parent_task_id
ON todos(parent_task_id)
WHERE parent_task_id IS NOT NULL;

-- Index for todos priority filtering
CREATE INDEX IF NOT EXISTS idx_todos_priority
ON todos(priority);

-- Indexes for task_events queries
CREATE INDEX IF NOT EXISTS idx_task_events_task_id
ON task_events(task_id);

CREATE INDEX IF NOT EXISTS idx_task_events_user_id
ON task_events(user_id);

CREATE INDEX IF NOT EXISTS idx_task_events_created_at
ON task_events(created_at);

CREATE INDEX IF NOT EXISTS idx_task_events_event_type
ON task_events(event_type);

-- Index for tags user lookup
CREATE INDEX IF NOT EXISTS idx_tags_user_id
ON tags(user_id);

-- ============================================================================
-- STEP 6: Add constraints
-- ============================================================================

-- Ensure priority is valid
ALTER TABLE todos
DROP CONSTRAINT IF EXISTS check_priority_valid;

ALTER TABLE todos
ADD CONSTRAINT check_priority_valid
CHECK (priority IN ('low', 'medium', 'high'));

-- Ensure recurrence_rule is valid
ALTER TABLE todos
DROP CONSTRAINT IF EXISTS check_recurrence_rule_valid;

ALTER TABLE todos
ADD CONSTRAINT check_recurrence_rule_valid
CHECK (recurrence_rule IS NULL OR recurrence_rule IN ('daily', 'weekly', 'monthly'));

-- Ensure recurrence_interval is positive
ALTER TABLE todos
DROP CONSTRAINT IF EXISTS check_recurrence_interval_positive;

ALTER TABLE todos
ADD CONSTRAINT check_recurrence_interval_positive
CHECK (recurrence_interval >= 1);

-- Ensure event_type is valid
ALTER TABLE task_events
DROP CONSTRAINT IF EXISTS check_event_type_valid;

ALTER TABLE task_events
ADD CONSTRAINT check_event_type_valid
CHECK (event_type IN ('task.created', 'task.updated', 'task.completed', 'task.deleted'));

COMMIT;

-- ============================================================================
-- Verification queries (run after migration)
-- ============================================================================

-- SELECT column_name, data_type, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'todos'
-- ORDER BY ordinal_position;

-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
-- AND table_name IN ('tags', 'todo_tags', 'task_events');
