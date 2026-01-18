# Data Model: Toggle Task Completion

**Feature**: 002-mark-complete | **Date**: 2026-01-13 | **Status**: Complete

## Overview

This feature operates on the existing Task entity from 001-add-task without schema modifications. The toggle operation updates a single field (`completed`) while preserving all other task attributes.

## Entities

### Task (Existing - No Changes)

**Source**: Inherited from 001-add-task (src/models.py)

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int                    # Unique sequential identifier
    title: str                 # Required task title
    description: str | None    # Optional task description
    completed: bool            # ⚡ Modified by toggle_task_completion()
    created_at: datetime       # Task creation timestamp
```

**Field Specifications**:

| Field | Type | Mutable? | Modified by 002? | Notes |
|-------|------|----------|------------------|-------|
| `id` | int | ❌ No | ❌ No | Set once at creation, never changed |
| `title` | str | ❌ No | ❌ No | Set at creation, immutable |
| `description` | str \| None | ❌ No | ❌ No | Set at creation, immutable |
| `completed` | bool | ✅ Yes | ✅ **YES** | **Toggled False↔True by this feature** |
| `created_at` | datetime | ❌ No | ❌ No | Set once at creation, never changed |

**Invariants**:
1. `id` is unique and sequential (enforced by storage layer)
2. `title` is never empty or None (enforced at creation)
3. `created_at` is set once and immutable
4. **`completed` can transition freely between False and True** (new invariant for 002)

**State Transitions**:
```
Initial State (from add_task):
    completed = False

After toggle_task_completion():
    completed = not completed

State Machine:
    False ⇄ True  (bidirectional toggle)
```

**No Schema Changes Required**:
- Task dataclass definition remains identical to 001-add-task
- No new fields added
- No fields removed
- No type changes
- Perfect backward compatibility

---

## Storage Schema (Existing - No Changes)

**Source**: Inherited from 001-add-task (src/storage.py)

```python
# Module-level storage
_tasks: list[Task] = []           # Ordered list of all tasks
_task_id_counter: int = 0         # Sequential ID generator
```

**Storage Invariants** (from ADR-0002):
1. Tasks are stored in creation order
2. List is append-only (tasks not removed by this feature)
3. Task objects are mutable (completed field can change)
4. No indexing structures (linear search used)

**Access Patterns**:
- **001-add-task**: Appends new Task to _tasks
- **002-mark-complete**: Searches _tasks, modifies Task.completed in-place

**Concurrency**: Single-threaded only (no locking required)

---

## Data Flow

### Toggle Operation Data Flow

```
Input: task_id (int)
    ↓
[1] Search _tasks list for matching Task.id
    ↓
[2a] If found → Task object reference
[2b] If not found → ValueError
    ↓
[3] Read current Task.completed value
    ↓
[4] Toggle: Task.completed = not Task.completed
    ↓
[5] Read NEW Task.completed value
    ↓
[6a] Print confirmation message (based on new value)
[6b] Create return dictionary (all fields)
    ↓
Output: dict[str, Any] with all task fields
```

**Data Mutation**:
- **Modified**: Task.completed field (in-place mutation)
- **Unchanged**: All other Task fields (id, title, description, created_at)
- **Storage**: _tasks list reference unchanged (same list, modified element)

---

## Function Contracts

### toggle_task_completion()

**Signature**:
```python
def toggle_task_completion(task_id: int) -> dict[str, Any]:
```

**Preconditions**:
- task_id is a positive integer
- _tasks list exists (initialized by 001-add-task)

**Postconditions (Success)**:
- Task with given ID has completed field toggled
- All other task fields unchanged
- Confirmation message printed to console
- Dictionary with all task fields returned

**Postconditions (Failure)**:
- No tasks modified
- Error message printed to console
- ValueError raised with descriptive message

**Side Effects**:
- Prints to stdout (console message)
- Mutates Task object in _tasks list (completed field only)

**Exceptions**:
- `ValueError`: Task with given ID not found

**Input Contract**:
```python
# Valid inputs
task_id: int  # Any positive integer (1, 2, 3, ...)

# Invalid inputs (not validated - caller responsibility)
task_id: int  # Zero or negative (undefined behavior)
task_id: str  # Type error (Python will raise TypeError)
```

**Output Contract**:
```python
# Return value (success case)
{
    'id': int,                    # Same as input task_id
    'title': str,                 # Unchanged from creation
    'description': str | None,    # Unchanged from creation
    'completed': bool,            # ← Toggled value (NEW state)
    'created_at': datetime        # Unchanged from creation
}

# Exception (failure case)
ValueError: "Task #{task_id} not found"
```

**Console Output Contract**:
```python
# Success cases
"✓ Task #{id} marked as complete"    # When toggled False→True
"✓ Task #{id} marked as incomplete"  # When toggled True→False

# Failure case
"✗ Error: Task #{id} not found"      # When task doesn't exist
```

---

## Data Validation

### Input Validation

**task_id validation**:
- ✅ Type: int (enforced by Python type hints)
- ✅ Range: Positive integer (1, 2, 3, ...)
- ❌ Not validated: Zero, negative (undefined behavior, out of scope)

**Why minimal validation?**
- Spec only requires handling non-existent IDs (FR-002, FR-008, FR-009)
- Caller responsibility to provide valid positive integers
- Consistent with 001-add-task validation philosophy (validate business rules, not types)

### Output Validation

**Return dictionary validation**:
- ✅ All required keys present (id, title, description, completed, created_at)
- ✅ Types match Task field types
- ✅ Values match current Task state

**Invariant checks** (for testing):
```python
# After toggle_task_completion(task_id)
assert result['id'] == task_id
assert result['title'] == original_title        # Unchanged
assert result['description'] == original_desc   # Unchanged
assert result['created_at'] == original_date    # Unchanged
assert result['completed'] != original_completed  # Changed!
```

---

## Field Preservation Guarantees

**Critical Requirement**: FR-007 specifies all non-completed fields MUST remain unchanged.

**Test Matrix**:

| Field | Before Toggle | After Toggle | Test Required? |
|-------|---------------|--------------|----------------|
| id | 1 | 1 | ✅ Yes (SC-004) |
| title | "Test" | "Test" | ✅ Yes (SC-004) |
| description | "Desc" | "Desc" | ✅ Yes (SC-004) |
| description | None | None | ✅ Yes (edge case) |
| created_at | 2026-01-13T10:00:00 | 2026-01-13T10:00:00 | ✅ Yes (SC-004) |
| completed | False | True | ✅ Yes (SC-002) |
| completed | True | False | ✅ Yes (SC-002) |

**Validation Method** (SC-004):
```python
# Before toggle
before = get_task_copy(task_id)

# Toggle operation
result = toggle_task_completion(task_id)

# After toggle - verify preservation
assert result['id'] == before['id']
assert result['title'] == before['title']
assert result['description'] == before['description']
assert result['created_at'] == before['created_at']
# Only completed should differ
assert result['completed'] != before['completed']
```

---

## Performance Considerations

### Time Complexity

**toggle_task_completion() operation**:
```
O(n) - Linear search through _tasks list
  + O(1) - Boolean toggle
  + O(1) - String formatting (message)
  + O(1) - Dictionary creation (5 fields)
  = O(n) total
```

**Where n = number of tasks in _tasks**:
- n = 100: ~0.1ms
- n = 500: ~0.5ms
- n = 1000: ~1ms

**Target**: <10ms (SC-006) ← 10x safety margin

### Space Complexity

**Memory Usage**:
- O(1) - No additional data structures
- Return dictionary: ~200 bytes (5 fields)
- No task copying (operates on reference)

**Total Memory Impact**: Negligible (~200 bytes per call)

### Scalability

**Current Scale**: <1000 tasks per session (inherited from 001-add-task)

**Scalability Limits**:
- Linear search becomes noticeable at ~5000 tasks (~5ms)
- If needed, could add dictionary index: {id: Task}
- Not needed for Phase I scope

---

## Integration with 001-add-task

### Shared Data Structures

**Both features operate on**:
- `_tasks: list[Task]` - Shared storage
- `Task` dataclass - Shared entity

**Dependency Graph**:
```
001-add-task (MUST exist first)
    ↓
    Creates: src/models.py (Task dataclass)
    Creates: src/storage.py (_tasks list)
    Creates: tests/conftest.py (pytest fixtures)
    ↓
002-mark-complete (builds on top)
    ↓
    Imports: Task from src/models.py
    Imports: _tasks from src/storage.py
    Uses: Existing test infrastructure
```

### Data Compatibility

**Perfect Compatibility**:
- 002 operates on Task objects created by 001
- No schema changes required
- No data migration needed
- Both features coexist without conflict

**Integration Test Pattern**:
```python
# Create task with 001-add-task
task = add_task("Test task", "Description")
assert task['completed'] == False  # Default

# Toggle with 002-mark-complete
result = toggle_task_completion(task['id'])
assert result['completed'] == True  # Toggled

# Toggle again
result2 = toggle_task_completion(task['id'])
assert result2['completed'] == False  # Toggled back
```

---

## Data Model Summary

**Key Points**:
1. **No schema changes** - Reuses Task dataclass as-is
2. **Single field mutation** - Only `completed` modified
3. **Field preservation** - All other fields immutable (FR-007)
4. **Bidirectional toggle** - False↔True state transitions
5. **Perfect compatibility** - Works with 001-add-task infrastructure
6. **Minimal complexity** - No new data structures or indexes
7. **Performance adequate** - O(n) search sufficient at scale

**Design Philosophy**:
- Reuse over reinvention
- Simplicity over optimization
- Compatibility over features
- Testability over cleverness

**Next**: See quickstart.md for TDD implementation guide
