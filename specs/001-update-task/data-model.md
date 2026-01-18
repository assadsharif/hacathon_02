# Data Model: Update Task

**Feature**: 001-update-task
**Date**: 2026-01-14
**Purpose**: Document data structures, field semantics, and state transitions

---

## Entity: Task

**Source**: Inherited from 001-add-task (`src/models.py`)

**No modifications required** - update-task reuses the existing Task dataclass without any schema changes.

### Task Dataclass

```python
@dataclass
class Task:
    """Represents a task in the todo list."""
    id: int                    # Unique sequential identifier
    title: str                 # Task title (required, non-empty)
    description: str | None    # Optional detailed description
    completed: bool            # Completion status
    created_at: datetime       # Creation timestamp
```

### Field Semantics for update_task

| Field | Type | Mutability | Update Behavior |
|-------|------|------------|-----------------|
| `id` | `int` | **IMMUTABLE** | Never modified by update_task |
| `title` | `str` | **MUTABLE** | Can be updated; must be non-empty after strip |
| `description` | `str \| None` | **MUTABLE** | Can be updated; can be set to None (clear) |
| `completed` | `bool` | **IMMUTABLE** | Use toggle_task_completion instead |
| `created_at` | `datetime` | **IMMUTABLE** | Never modified (preserves original creation time) |

### Field Constraints

**title**:
- **Type**: `str`
- **Required**: When provided for update (optional parameter)
- **Validation**: Must be non-empty after stripping whitespace
- **Normalization**: Leading/trailing whitespace stripped
- **Error**: "Task title cannot be empty" if empty/whitespace-only
- **Examples**:
  - ✅ Valid: `"Buy groceries"`, `"  Task with spaces  "` (stripped to `"Task with spaces"`)
  - ❌ Invalid: `""`, `"   "`, `"\t\n"` (empty after stripping)

**description**:
- **Type**: `str | None`
- **Required**: Optional (can omit from update)
- **Validation**: None (any string or None accepted)
- **Special Behavior**: Can be set to `None` to clear description
- **Examples**:
  - ✅ Valid: `"Detailed description"`, `""`, `None` (clears description)

**id, completed, created_at**:
- **Immutability**: These fields are **never** modified by update_task
- **Rationale**:
  - `id`: Identity - changing would break references
  - `completed`: Use toggle_task_completion (002-mark-complete) instead
  - `created_at`: Historical record - should reflect original creation time

---

## State Transitions

### Successful Update Transitions

**Scenario 1: Update Title Only**
```
BEFORE: Task(id=1, title="Old Title", description="Description", completed=False, created_at=2026-01-14T10:00:00)
ACTION: update_task(1, title="New Title")
AFTER:  Task(id=1, title="New Title", description="Description", completed=False, created_at=2026-01-14T10:00:00)
CHANGED: title
PRESERVED: id, description, completed, created_at
```

**Scenario 2: Update Description Only**
```
BEFORE: Task(id=2, title="Task Title", description="Old Desc", completed=True, created_at=2026-01-14T10:00:00)
ACTION: update_task(2, description="New Description")
AFTER:  Task(id=2, title="Task Title", description="New Description", completed=True, created_at=2026-01-14T10:00:00)
CHANGED: description
PRESERVED: id, title, completed, created_at
```

**Scenario 3: Update Both Fields**
```
BEFORE: Task(id=3, title="Old", description="Old Desc", completed=False, created_at=2026-01-14T10:00:00)
ACTION: update_task(3, title="New", description="New Desc")
AFTER:  Task(id=3, title="New", description="New Desc", completed=False, created_at=2026-01-14T10:00:00)
CHANGED: title, description
PRESERVED: id, completed, created_at
```

**Scenario 4: Clear Description**
```
BEFORE: Task(id=4, title="Task", description="Some description", completed=False, created_at=2026-01-14T10:00:00)
ACTION: update_task(4, description=None)
AFTER:  Task(id=4, title="Task", description=None, completed=False, created_at=2026-01-14T10:00:00)
CHANGED: description (set to None)
PRESERVED: id, title, completed, created_at
```

**Scenario 5: Multiple Updates to Same Task**
```
INITIAL: Task(id=5, title="Original", description="Original Desc", completed=False, created_at=2026-01-14T10:00:00)

UPDATE 1: update_task(5, title="First Update")
STATE:    Task(id=5, title="First Update", description="Original Desc", completed=False, created_at=2026-01-14T10:00:00)

UPDATE 2: update_task(5, description="Second Update")
STATE:    Task(id=5, title="First Update", description="Second Update", completed=False, created_at=2026-01-14T10:00:00)

UPDATE 3: update_task(5, title="Final", description="Final Desc")
FINAL:    Task(id=5, title="Final", description="Final Desc", completed=False, created_at=2026-01-14T10:00:00)

PRESERVED THROUGHOUT: id=5, completed=False, created_at=2026-01-14T10:00:00
```

### Error State Transitions

**Error Condition 1: No Fields Provided**
```
BEFORE: Task(id=1, title="Title", description="Desc", completed=False, created_at=T)
ACTION: update_task(1)  # No title or description
RESULT: ValueError("No fields to update")
AFTER:  Task(id=1, title="Title", description="Desc", completed=False, created_at=T)  # UNCHANGED
```

**Error Condition 2: Task Not Found**
```
STORAGE: [Task(id=1, ...), Task(id=2, ...)]  # No task with id=999
ACTION:  update_task(999, title="New")
RESULT:  ValueError("Task #999 not found")
AFTER:   [Task(id=1, ...), Task(id=2, ...)]  # UNCHANGED
```

**Error Condition 3: Empty Title**
```
BEFORE: Task(id=1, title="Original", description="Desc", completed=False, created_at=T)
ACTION: update_task(1, title="   ")  # Whitespace-only
RESULT: ValueError("Task title cannot be empty")
AFTER:  Task(id=1, title="Original", description="Desc", completed=False, created_at=T)  # UNCHANGED
```

**Atomicity Guarantee**: On any error, **no fields are modified**. All validations occur before any state changes.

---

## Storage Model

**Location**: `src/storage.py` (existing module, no changes)

```python
# Module-level in-memory storage
_tasks: list[Task] = []
_task_id_counter: int = 0
```

**update_task Behavior**:
- **Read**: Linear search through `_tasks` to find task by `id`
- **Write**: In-place mutation of task object fields
- **Concurrency**: None (single-threaded console application)
- **Persistence**: None (in-memory only, reset on restart)

**Relationship to Storage**:
- `update_task` **does not** use `_task_id_counter` (only add_task uses it)
- `update_task` **does not** add/remove tasks from `_tasks` (only modifies existing)
- `update_task` relies on task objects being mutable (not frozen dataclasses)

---

## Validation Rules

### Pre-Condition Validations (before any updates)

**V1: At Least One Field Provided**
```python
if title is None and description is None:
    raise ValueError("No fields to update")
```
- **Timing**: First validation (cheapest)
- **Rationale**: Prevent no-op calls

**V2: Task Exists**
```python
task = next((t for t in _tasks if t.id == task_id), None)
if task is None:
    raise ValueError(f"Task #{task_id} not found")
```
- **Timing**: Second validation (requires storage lookup)
- **Rationale**: Ensure target task exists before validating field values

**V3: Title Non-Empty (if provided)**
```python
if title is not None:
    title_stripped = title.strip()
    if not title_stripped:
        raise ValueError("Task title cannot be empty")
```
- **Timing**: Third validation (only if title provided)
- **Rationale**: Ensure data quality for title field

### Post-Condition Guarantees

After successful update_task call:
1. ✅ Exactly the specified fields are updated
2. ✅ All other fields remain unchanged
3. ✅ Confirmation message printed to stdout
4. ✅ Dictionary with all task fields returned
5. ✅ Task remains in same position in `_tasks` list

After failed update_task call (ValueError raised):
1. ✅ No fields modified (atomicity)
2. ✅ Error message printed to stdout
3. ✅ ValueError raised with descriptive message
4. ✅ Storage state unchanged

---

## Integration with Other Features

### 001-add-task → 001-update-task

```python
# Create task
task_dict = add_task("Original Title", "Original Description")
# ✓ Task #1 added: Original Title
# task_dict = {'id': 1, 'title': 'Original Title', 'description': 'Original Description', ...}

# Update task
updated_dict = update_task(1, title="Updated Title")
# ✓ Task #1 updated successfully
# updated_dict = {'id': 1, 'title': 'Updated Title', 'description': 'Original Description', ...}
```

**Data Flow**: add_task creates Task → update_task modifies fields → Task object shared

### 001-update-task + 002-mark-complete

```python
# Update title
update_task(1, title="New Title")

# Toggle completion (independent operation)
toggle_task_completion(1)
# Completion status changes, title remains "New Title"
```

**Field Isolation**: update_task modifies title/description, toggle_task_completion modifies completed - no conflicts

### 001-update-task + 003-delete-task

```python
# Update task
update_task(1, description="Updated")

# Delete task
delete_task(1)
# Task removed from storage (updates lost - expected behavior)
```

**Lifecycle**: update_task operates on living tasks; delete_task removes them

---

## Data Model Summary

**Entity**: Task (inherited, no changes)
**Mutable Fields**: title, description
**Immutable Fields**: id, completed, created_at
**Storage**: In-memory list (`_tasks`)
**Validation**: Fail-fast (fields → existence → title)
**Atomicity**: All-or-nothing updates
**Integration**: Extends add_task workflow, compatible with toggle/delete

**Next Phase**: Generate API contracts and quickstart guide
