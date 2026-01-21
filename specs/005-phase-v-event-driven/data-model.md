# Phase V Data Model

**Date**: 2026-01-20 | **Branch**: `005-phase-v-event-driven`

## Overview

Phase V extends the existing Todo model with advanced task features and introduces new entities for event-driven architecture.

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────────────┐       ┌──────────────┐
│    User     │       │        Todo         │       │     Tag      │
├─────────────┤       ├─────────────────────┤       ├──────────────┤
│ id (UUID)   │◀──────│ user_id (FK)        │       │ id (int)     │
│ email       │   1:N │ id (int)            │       │ name (str)   │
│ name        │       │ title               │       │ user_id (FK) │
│ created_at  │       │ description         │       └──────┬───────┘
└─────────────┘       │ status              │              │
                      │ priority     [NEW]  │              │ N:M
                      │ due_date     [NEW]  │       ┌──────┴───────┐
                      │ recurrence   [NEW]  │       │  TodoTag     │
                      │ reminder_at  [NEW]  │       ├──────────────┤
                      │ created_at          │       │ todo_id (FK) │
                      │ updated_at          │◀──────│ tag_id (FK)  │
                      └─────────────────────┘       └──────────────┘
                               │
                               │ 1:N (events)
                               ▼
                      ┌─────────────────────┐
                      │    TaskEvent        │
                      ├─────────────────────┤
                      │ id (UUID)           │
                      │ task_id (FK)        │
                      │ user_id (FK)        │
                      │ event_type          │
                      │ payload (JSON)      │
                      │ created_at          │
                      └─────────────────────┘
```

---

## Extended Entities

### Todo (Extended)

**Table**: `todos`

| Field | Type | Constraints | Description | Phase |
|-------|------|-------------|-------------|-------|
| `id` | `INT` | PK, AUTO | Primary key | II |
| `user_id` | `UUID` | FK→users, NOT NULL | Owner | II |
| `title` | `VARCHAR(200)` | NOT NULL | Task title | II |
| `description` | `TEXT` | NULLABLE | Task description | II |
| `status` | `VARCHAR(20)` | DEFAULT 'active' | "active", "completed" | II |
| `priority` | `VARCHAR(10)` | DEFAULT 'medium' | "low", "medium", "high" | **V** |
| `due_date` | `TIMESTAMP` | NULLABLE | When task is due | **V** |
| `reminder_at` | `TIMESTAMP` | NULLABLE | When to send reminder | **V** |
| `recurrence_rule` | `VARCHAR(20)` | NULLABLE | "daily", "weekly", "monthly" | **V** |
| `recurrence_interval` | `INT` | DEFAULT 1 | Repeat every N periods | **V** |
| `recurrence_end_date` | `TIMESTAMP` | NULLABLE | When recurrence stops | **V** |
| `parent_task_id` | `INT` | FK→todos, NULLABLE | For recurring instances | **V** |
| `created_at` | `TIMESTAMP` | NOT NULL | Creation time | II |
| `updated_at` | `TIMESTAMP` | NOT NULL | Last update time | II |

**Indexes**:
- `idx_todos_user_id` on `user_id`
- `idx_todos_due_date` on `due_date` (for reminder queries)
- `idx_todos_parent_task_id` on `parent_task_id` (for recurring tasks)

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from typing import Optional, Literal
import uuid

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    # Existing fields (Phase II)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="active", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # NEW: Phase V fields
    priority: str = Field(default="medium", max_length=10)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    reminder_at: Optional[datetime] = Field(default=None)
    recurrence_rule: Optional[str] = Field(default=None, max_length=20)  # daily, weekly, monthly
    recurrence_interval: int = Field(default=1)
    recurrence_end_date: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("todos.id"), nullable=True)
    )
```

---

### Tag (New)

**Table**: `tags`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `INT` | PK, AUTO | Primary key |
| `name` | `VARCHAR(50)` | NOT NULL | Tag name |
| `user_id` | `UUID` | FK→users, NOT NULL | Tag owner |
| `created_at` | `TIMESTAMP` | NOT NULL | Creation time |

**Unique Constraint**: `(name, user_id)` - Each user has unique tag names.

**SQLModel Definition**:

```python
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, min_length=1)
    user_id: Optional[uuid.UUID] = Field(
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_args = (UniqueConstraint("name", "user_id"),)
```

---

### TodoTag (Junction Table)

**Table**: `todo_tags`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `todo_id` | `INT` | FK→todos, PK | Todo reference |
| `tag_id` | `INT` | FK→tags, PK | Tag reference |

**SQLModel Definition**:

```python
class TodoTag(SQLModel, table=True):
    __tablename__ = "todo_tags"

    todo_id: int = Field(foreign_key="todos.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

---

### TaskEvent (Audit Log)

**Table**: `task_events` (immutable append-only)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `UUID` | PK | Event ID |
| `task_id` | `INT` | NOT NULL | Task reference (no FK for decoupling) |
| `user_id` | `UUID` | NOT NULL | User reference (no FK for decoupling) |
| `event_type` | `VARCHAR(20)` | NOT NULL | Event type |
| `payload` | `JSONB` | NOT NULL | Event data snapshot |
| `created_at` | `TIMESTAMP` | NOT NULL | Event time |

**Event Types**: `task.created`, `task.updated`, `task.completed`, `task.deleted`

**SQLModel Definition**:

```python
from sqlalchemy.dialects.postgresql import JSONB

class TaskEvent(SQLModel, table=True):
    __tablename__ = "task_events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: int = Field(index=True)
    user_id: uuid.UUID = Field(index=True)
    event_type: str = Field(max_length=20)  # task.created, task.updated, etc.
    payload: dict = Field(sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

---

## Event Schema (CloudEvents)

### Base Event Structure

```json
{
  "specversion": "1.0",
  "type": "task.created",
  "source": "/todo-chatbot/backend",
  "id": "evt-550e8400-e29b-41d4-a716-446655440000",
  "time": "2026-01-20T12:00:00Z",
  "datacontenttype": "application/json",
  "data": { ... }
}
```

### Event Type: `task.created`

```json
{
  "data": {
    "taskId": 123,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": null,
    "status": "active",
    "priority": "high",
    "dueDate": 1737367200,
    "reminderAt": 1737363600,
    "recurrence": {
      "rule": "weekly",
      "interval": 1,
      "endDate": null
    },
    "tags": ["shopping", "personal"],
    "createdAt": 1737280800
  }
}
```

### Event Type: `task.updated`

```json
{
  "data": {
    "taskId": 123,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "changes": {
      "title": { "old": "Buy groceries", "new": "Buy organic groceries" },
      "priority": { "old": "medium", "new": "high" }
    },
    "updatedAt": 1737367200
  }
}
```

### Event Type: `task.completed`

```json
{
  "data": {
    "taskId": 123,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "isRecurring": true,
    "recurrence": {
      "rule": "weekly",
      "interval": 1
    },
    "completedAt": 1737367200
  }
}
```

### Event Type: `task.deleted`

```json
{
  "data": {
    "taskId": 123,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "deletedAt": 1737367200
  }
}
```

---

## Validation Rules

### Priority
- Valid values: `"low"`, `"medium"`, `"high"`
- Default: `"medium"`

### Recurrence Rule
- Valid values: `"daily"`, `"weekly"`, `"monthly"`, `null`
- If set, `recurrence_interval` must be >= 1
- `recurrence_end_date` is optional (infinite recurrence if null)

### Due Date & Reminder
- `reminder_at` must be before or equal to `due_date`
- If `reminder_at` is set but `due_date` is not, auto-set `due_date` = `reminder_at`

### Tags
- Maximum 10 tags per todo
- Tag name: 1-50 characters, alphanumeric and hyphens only

---

## State Transitions

### Task Status

```
                 ┌───────────────┐
                 │    active     │
                 └───────┬───────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌─────────────────┐           ┌─────────────────┐
│    completed    │           │     deleted     │
└─────────────────┘           └─────────────────┘
          │
          │ (if recurring)
          ▼
┌─────────────────┐
│  new instance   │──▶ (repeat cycle)
│    (active)     │
└─────────────────┘
```

### Recurring Task Flow

1. User completes recurring task
2. `task.completed` event published
3. Recurring service consumes event
4. If `recurrence_rule` is set and within `recurrence_end_date`:
   - Calculate next occurrence date
   - Create new task instance with `parent_task_id` set
   - Publish `task.created` event for new instance

---

## Migration Script

```sql
-- Phase V Migration: Add advanced task features

-- Add new columns to todos table
ALTER TABLE todos
ADD COLUMN priority VARCHAR(10) DEFAULT 'medium',
ADD COLUMN due_date TIMESTAMP,
ADD COLUMN reminder_at TIMESTAMP,
ADD COLUMN recurrence_rule VARCHAR(20),
ADD COLUMN recurrence_interval INT DEFAULT 1,
ADD COLUMN recurrence_end_date TIMESTAMP,
ADD COLUMN parent_task_id INT REFERENCES todos(id);

-- Create tags table
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(name, user_id)
);

-- Create junction table for many-to-many
CREATE TABLE IF NOT EXISTS todo_tags (
    todo_id INT NOT NULL REFERENCES todos(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (todo_id, tag_id)
);

-- Create task_events table for audit log
CREATE TABLE IF NOT EXISTS task_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id INT NOT NULL,
    user_id UUID NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_todos_due_date ON todos(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_todos_parent_task_id ON todos(parent_task_id) WHERE parent_task_id IS NOT NULL;
CREATE INDEX idx_task_events_task_id ON task_events(task_id);
CREATE INDEX idx_task_events_user_id ON task_events(user_id);
CREATE INDEX idx_task_events_created_at ON task_events(created_at);
```
