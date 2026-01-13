# Data Model: Delete Task by ID

**Feature**: 003-delete-task | **Created**: 2026-01-13 | **Status**: Complete

## Purpose

This document defines the data structures, contracts, and data flow for the delete task feature. The feature operates on existing entities from 001-add-task and introduces no new data models.

## Entities

### Task (Existing from 001-add-task)

**Source**: `src/models.py` (defined in 001-add-task)

**Definition**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int                    # Unique sequential identifier (1, 2, 3...)
    title: str                 # Required, non-empty after strip
    description: str | None    # Optional, accepts any string or None
    completed: bool            # Task completion status
    created_at: datetime       # Auto-generated timestamp
```

**Attributes**:

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| `id` | `int` | Positive integer starting from 1, unique, sequential | Primary identifier for task lookup and deletion |
| `title` | `str` | Non-empty after strip, required | Task name displayed in confirmation message |
| `description` | `str \| None` | Optional, any string or None | Additional task details (included in return value) |
| `completed` | `bool` | Required, defaults to False | Task completion status (captured before deletion) |
| `created_at` | `datetime` | Auto-generated, immutable | Task creation timestamp (audit trail) |

**Invariants** (enforced by 001-add-task, preserved by delete):
1. `id` is always unique and positive (never reused after deletion)
2. `title` is never empty or None
3. `created_at` is set once at creation and never modified
4. Task objects are immutable except for `completed` field (via toggle_task_completion)

**Operations on Task**:
- **Read**: Task is read from storage during lookup by ID
- **Delete**: Task is removed from storage (permanent)
- **Capture**: All fields copied to dictionary before deletion (audit trail)

## Storage Schema

**Source**: `src/storage.py` (defined in 001-add-task)

**Module-Level Variables**:

```python
_tasks: list[Task] = []        # Ordered list of all tasks
_task_id_counter: int = 0      # Monotonically increasing counter
```

**Storage Characteristics**:
- In-memory only (no persistence)
- Single module-level list maintains insertion order
- Direct object reference storage (not serialized)
- O(n) search, O(n) deletion complexity

**Impact of Deletion on Storage**:
1. **Task removal**: Target task removed from `_tasks` list
2. **Counter preservation**: `_task_id_counter` never decrements (deleted IDs not reused)
3. **Index shift**: List indices shift after deletion (task objects unchanged)
4. **No cascade**: No other storage effects (no dependent entities)

**Storage State Transition**:

```
BEFORE deletion (task ID 2 exists):
_tasks = [Task(id=1, ...), Task(id=2, ...), Task(id=3, ...)]
_task_id_counter = 3

AFTER delete_task(2):
_tasks = [Task(id=1, ...), Task(id=3, ...)]
_task_id_counter = 3  # Unchanged - no ID reuse
```

## Function Contract

### delete_task()

**Location**: `src/task_manager.py` (new function in this feature)

**Signature**:
```python
def delete_task(task_id: int) -> dict[str, Any]:
```

**Input Contract**:

| Parameter | Type | Constraints | Validation |
|-----------|------|-------------|------------|
| `task_id` | `int` | Must be positive integer | Validated implicitly during lookup (not found if invalid) |

**Output Contract**:

| Output | Type | Content | When |
|--------|------|---------|------|
| Return value | `dict[str, Any]` | All task fields before deletion | On success |
| Print output | `str` | `"✓ Task #{id} deleted: {title}"` | On success |
| Exception | `ValueError` | `"Task #{id} not found"` | On task not found |
| Print output | `str` | `"✗ Error: Task #{id} not found"` | On task not found |

**Return Dictionary Schema**:
```python
{
    'id': int,                    # Task ID that was deleted
    'title': str,                 # Task title (for confirmation)
    'description': str | None,    # Task description (may be None)
    'completed': bool,            # Completion status before deletion
    'created_at': datetime        # Creation timestamp
}
```

**Preconditions**:
1. `_tasks` list is initialized (from 001-add-task setup)
2. `task_id` is an integer (enforced by type hint)
3. Function is called after at least one task has been added (if deleting existing task)

**Postconditions (Success Path)**:
1. Task with matching `task_id` is removed from `_tasks`
2. All other tasks remain in `_tasks` with unchanged data
3. Return dictionary contains all fields from deleted task
4. Confirmation message printed to console
5. `_task_id_counter` unchanged (no ID reuse)

**Postconditions (Error Path)**:
1. No tasks removed from `_tasks`
2. Storage state unchanged
3. ValueError raised with descriptive message
4. Error message printed to console

**Side Effects**:
1. **Storage mutation**: Task permanently removed from `_tasks` list
2. **Console output**: Confirmation or error message printed
3. **No undo**: Deletion is permanent (cannot be reversed)

## Data Flow

### Success Path: Delete Existing Task

```
[1] User calls delete_task(task_id=2)
     ↓
[2] Function searches _tasks list for task with id=2
     ↓
[3] Task found at index i
     ↓
[4] Capture all task fields to dictionary:
     deleted_data = {
       'id': task.id,
       'title': task.title,
       'description': task.description,
       'completed': task.completed,
       'created_at': task.created_at
     }
     ↓
[5] Remove task from storage: _tasks.remove(task)
     ↓
[6] Print confirmation: "✓ Task #2 deleted: {task.title}"
     ↓
[7] Return deleted_data dictionary
     ↓
[8] User receives return value (for audit/logging)
```

### Error Path: Task Not Found

```
[1] User calls delete_task(task_id=999)
     ↓
[2] Function searches _tasks list for task with id=999
     ↓
[3] Task NOT found (loop completes, task=None)
     ↓
[4] Print error: "✗ Error: Task #999 not found"
     ↓
[5] Raise ValueError("Task #999 not found")
     ↓
[6] Exception propagates to caller
     ↓
[7] Storage unchanged (_tasks not modified)
```

## Integration with Existing Features

### Dependency: 001-add-task

**Required Components**:
1. **Task dataclass**: Defines structure of tasks to be deleted
2. **Storage infrastructure**: `_tasks` list and `_task_id_counter`
3. **ID generation**: Sequential counter ensures no ID collisions

**Integration Points**:
- delete_task() operates on Task objects created by add_task()
- Deletion preserves ID uniqueness (deleted IDs never reused by add_task)
- Both functions share same `_tasks` storage

### Dependency: 002-mark-complete

**Reused Patterns**:
1. **Task lookup**: Linear search through `_tasks` list by ID
2. **Error handling**: ValueError with dual output (print + raise)
3. **Function structure**: Input validation → operation → output

**Integration Points**:
- Both functions can operate on the same tasks
- delete_task() can delete tasks that were toggled by toggle_task_completion()
- Error handling consistency across all features

### Cross-Feature Data Flow

```
[add_task] Creates task with id=1
    ↓
[toggle_task_completion] Modifies task.completed
    ↓
[delete_task] Removes task permanently
    ↓
[add_task] Creates new task with id=2 (no ID reuse)
```

## Validation Rules

### Input Validation

1. **Task ID type**: Must be `int` (enforced by type hint)
2. **Task ID existence**: Must match an existing task in storage
3. **No additional validation**: Negative IDs, zero, None handled by "not found" logic

### State Validation

1. **Storage non-interference**: Only target task removed, others preserved
2. **Counter preservation**: `_task_id_counter` never decrements
3. **Data capture accuracy**: Return dictionary must match task before deletion

### Output Validation

1. **Return dictionary completeness**: All 5 fields present (id, title, description, completed, created_at)
2. **Data type preservation**: datetime objects not serialized (remain as datetime)
3. **Message format**: Confirmation message includes ID and title

## Edge Cases and Handling

| Edge Case | Data Impact | Handling |
|-----------|-------------|----------|
| Delete only task in list | `_tasks` becomes empty | Success - returns task data, storage empty |
| Delete first task (index 0) | Indices shift down | Success - other tasks unaffected |
| Delete last task (final index) | No index shift for others | Success - other tasks unaffected |
| Delete middle task | Indices shift for tasks after | Success - other tasks unaffected |
| Delete with ID=0 | No task found | Error - ValueError raised |
| Delete with negative ID | No task found | Error - ValueError raised |
| Delete non-existent ID | No task found | Error - ValueError raised |
| Delete same ID twice | Second call finds nothing | Error - ValueError raised |
| Empty storage | No task found | Error - ValueError raised |

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Task lookup | O(n) | Linear search through `_tasks` list |
| Task removal | O(n) | `list.remove()` shifts elements |
| Data capture | O(1) | Dictionary creation with 5 fields |
| Total operation | O(n) | Dominated by search + removal |

### Space Complexity

| Aspect | Complexity | Notes |
|--------|------------|-------|
| Return dictionary | O(1) | Fixed 5 fields regardless of list size |
| Storage reduction | -O(1) | One task removed from memory |
| Temporary variables | O(1) | Loop variable, captured data |

### Expected Performance (SC-006)

- **Target**: <10ms per operation
- **100 tasks**: <1ms (search + removal)
- **500 tasks**: <2ms (search + removal)
- **1000 tasks**: <5ms (search + removal)
- **Margin**: 2-5x safety margin below 10ms target

## Testing Considerations

### Data Validation Tests

1. **Return dictionary completeness**: Verify all 5 fields present and correct
2. **Data type preservation**: Verify datetime not serialized
3. **Field accuracy**: Verify captured data matches task before deletion

### Storage State Tests

1. **Target deletion**: Only specified task removed
2. **Non-interference**: Other tasks unchanged (IDs, fields, order)
3. **Empty storage**: Deletion works correctly when list becomes empty
4. **Counter preservation**: `_task_id_counter` never decrements

### Integration Tests

1. **With add_task**: Delete tasks created by add_task
2. **With toggle_task_completion**: Delete tasks that were toggled
3. **ID reuse prevention**: Verify new tasks get unique IDs after deletion

## References

- **Spec**: [spec.md](./spec.md) - Feature requirements (FR-001 through FR-010)
- **Plan**: [plan.md](./plan.md) - Implementation approach and decisions
- **Research**: [research.md](./research.md) - Technical research and rationale
- **001-add-task**: Task dataclass and storage infrastructure
- **002-mark-complete**: Task lookup and error handling patterns
- **ADR-0001**: Python 3.13+ union type syntax (`str | None`)
- **ADR-0002**: In-memory list storage architecture
- **ADR-0003**: Sequential counter-based ID generation
