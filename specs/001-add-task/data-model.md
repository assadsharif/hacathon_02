# Data Model: Add Task Feature

**Feature**: 001-add-task
**Date**: 2026-01-10
**Status**: Complete

## Overview

This document defines the data model for the Add Task feature. All data is stored in-memory using Python data structures with no persistence layer.

## Entities

### Task

Represents a single task item in the todo list.

**Type**: Python `@dataclass`

**Attributes**:

| Attribute | Type | Required | Default | Description | Validation |
|-----------|------|----------|---------|-------------|------------|
| `id` | `int` | Yes | Auto-generated | Unique sequential identifier starting from 1 | Must be positive integer |
| `title` | `str` | Yes | - | Task title/summary | Non-empty after stripping whitespace |
| `description` | `str \| None` | No | `None` | Optional detailed description | Any string or None |
| `completed` | `bool` | Yes | `False` | Completion status flag | Boolean |
| `created_at` | `datetime` | Yes | Auto-generated | Creation timestamp | UTC datetime |

**Invariants**:
1. `id` is unique across all tasks
2. `id` values are sequential and increment by 1
3. `title` is never empty or None (enforced at creation)
4. `created_at` is set once at creation and never modified
5. `completed` defaults to False for new tasks

**Example**:
```python
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime(2026, 1, 10, 14, 30, 0)
)
```

### Implementation

**File**: `src/models.py`

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """
    Represents a task in the todo list.

    Attributes:
        id: Unique sequential identifier
        title: Task title (required, non-empty)
        description: Optional detailed description
        completed: Completion status (default: False)
        created_at: Creation timestamp (UTC)
    """
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
```

## Storage Schema

### Task Collection

**Type**: In-memory list
**Variable**: `_tasks` (module-level in `src/storage.py`)
**Access**: Private (prefix with `_`)

**Structure**:
```python
_tasks: list[Task] = []
```

**Operations**:
- **Append**: Add new task to end of list (O(1) amortized)
- **Read**: Access by index or iterate (O(1) or O(n))
- **Count**: `len(_tasks)` for total task count (O(1))

**Characteristics**:
- Ordered by creation time (append-only for this feature)
- No deletions in this feature (out of scope)
- No updates to existing tasks in this feature (out of scope)
- Data lost when application terminates (per constitution)

### ID Counter

**Type**: Module-level integer counter
**Variable**: `_task_id_counter` (module-level in `src/storage.py`)
**Access**: Private (prefix with `_`)

**Structure**:
```python
_task_id_counter: int = 0
```

**Behavior**:
- Initializes to 0
- Increments before assignment (first task gets ID 1)
- Never decrements
- Persists only during application runtime

## Data Flow

### Task Creation Flow

```
User Input (title, description)
        ↓
Validation (title non-empty)
        ↓
Generate ID (_task_id_counter++)
        ↓
Generate timestamp (datetime.now())
        ↓
Create Task object
        ↓
Append to _tasks list
        ↓
Return task dictionary
```

### Data Transformations

**Task → Dictionary** (for return value):
```python
{
    'id': task.id,
    'title': task.title,
    'description': task.description,
    'completed': task.completed,
    'created_at': task.created_at
}
```

This transformation enables:
- Easy serialization for display
- Flexible return format
- Decoupling from internal representation

## Validation Rules

### At Task Creation

**Title Validation** (enforced in `add_task()` function):
1. Must not be None
2. Must not be empty string
3. Must not be only whitespace (after `.strip()`)

**ID Validation** (enforced in ID generation):
1. Must be unique (guaranteed by counter increment)
2. Must be sequential (guaranteed by counter)
3. Must start at 1 (counter starts at 0, increments before use)

**Timestamp Validation**:
1. Always uses current UTC time
2. Uses `datetime.now()` for generation
3. Never modified after creation

**Description Validation**:
- None validation required
- Accepts any string value including empty string
- Accepts None value

### Data Integrity Constraints

1. **Uniqueness**: No two tasks can have the same ID
2. **Immutability**: Task ID and created_at never change after creation
3. **Ordering**: Tasks maintain insertion order in list
4. **Type Safety**: All attributes match type annotations

## Relationships

**Current Feature**: No relationships (single entity)

**Future Considerations** (out of scope for this feature):
- Task → User (when multi-user support added)
- Task → Category/Tag (when categorization added)
- Task → Subtask (when task hierarchy added)

## Migrations

Not applicable - in-memory storage has no persistence or versioning.

## Performance Characteristics

### Memory Usage

**Per Task**: ~200-500 bytes depending on string lengths
- `id`: 28 bytes (int object)
- `title`: ~50-100 bytes (typical string)
- `description`: ~100-500 bytes (typical string) or 16 bytes (None)
- `completed`: 28 bytes (bool object)
- `created_at`: 48 bytes (datetime object)

**Expected Scale**: <1000 tasks → <500 KB total memory

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Create task | O(1) | List append is amortized O(1) |
| Generate ID | O(1) | Counter increment |
| Validate title | O(n) | n = title length for strip() |
| Store task | O(1) | List append |

## Error Handling

### Validation Errors

**ValueError** raised when:
- Title is None
- Title is empty string
- Title is whitespace-only

**Error Messages**:
- `"Task title is required"` - Displayed to user
- Exception propagates to caller for programmatic handling

### Data Errors

**Prevention**:
- Type hints enforce correct types at development time
- Dataclass validates attribute types at runtime
- ID counter ensures uniqueness

**No Errors Expected For**:
- Description (accepts any string or None)
- Completed flag (bool type, defaults to False)
- Timestamp (auto-generated, always valid)

## Testing Considerations

### Unit Tests

Test the Task model:
- ✓ Create task with all fields
- ✓ Create task with minimal fields (title only)
- ✓ Validate ID uniqueness
- ✓ Validate title requirement
- ✓ Validate timestamp generation

### Integration Tests

Test storage operations:
- ✓ Add multiple tasks, verify IDs increment
- ✓ Verify tasks maintain insertion order
- ✓ Verify in-memory persistence during session

### Edge Cases

- Very long titles (1000+ characters)
- Unicode characters in title/description
- Special characters (emoji, symbols)
- Empty description vs None description

## Dependencies

**Standard Library**:
- `dataclasses` - Task model definition
- `datetime` - Timestamp generation
- `typing` - Type hints (built-in Python 3.13)

**No External Dependencies**

