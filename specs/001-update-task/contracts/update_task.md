# API Contract: update_task

**Feature**: 001-update-task
**Module**: `src.task_manager`
**Function**: `update_task`
**Date**: 2026-01-14

---

## Function Signature

```python
def update_task(
    task_id: int,
    *,
    title: str | None = None,
    description: str | None = None
) -> dict[str, Any]:
    """Update an existing task's title and/or description.

    Implements FR-001 through FR-015 from specs/001-update-task/spec.md.
    Provides dual output per established pattern:
    - Prints confirmation message to stdout (or error message on failure)
    - Returns dictionary with task details (or raises ValueError on failure)

    Args:
        task_id: The ID of the task to update (required, must exist in storage)
        title: New title for the task (optional, must be non-empty after stripping if provided)
        description: New description for the task (optional, can be None to clear description)

    Returns:
        Dictionary containing all task attributes:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If no fields provided, task ID not found, or title is empty/whitespace-only

    Examples:
        >>> task = add_task("Original Title", "Original Description")
        ✓ Task #1 added: Original Title

        >>> updated = update_task(1, title="New Title")
        ✓ Task #1 updated successfully
        >>> print(updated['title'])
        'New Title'
        >>> print(updated['description'])
        'Original Description'

        >>> updated = update_task(1, description="New Description")
        ✓ Task #1 updated successfully

        >>> updated = update_task(1, title="Both", description="Updated")
        ✓ Task #1 updated successfully

        >>> update_task(1, description=None)
        ✓ Task #1 updated successfully
        # Description is now None (cleared)

        >>> update_task(999, title="New")
        ✗ Error: Task #999 not found
        ValueError: Task #999 not found

        >>> update_task(1, title="")
        ✗ Error: Task title cannot be empty
        ValueError: Task title cannot be empty

        >>> update_task(1)
        ✗ Error: No fields to update
        ValueError: No fields to update
    """
```

---

## Input Contract

### Parameters

**task_id** (required, positional)
- **Type**: `int`
- **Validation**: Must correspond to an existing task in storage
- **Error**: ValueError("Task #{task_id} not found") if task doesn't exist
- **Examples**:
  - ✅ Valid: `1`, `2`, `100` (if tasks exist)
  - ❌ Invalid: `999` (if no task with ID 999), `0`, `-1`

**title** (optional, keyword-only)
- **Type**: `str | None`
- **Default**: `None` (not updated)
- **Validation**: If provided, must be non-empty after stripping whitespace
- **Normalization**: Leading/trailing whitespace stripped before storage
- **Error**: ValueError("Task title cannot be empty") if empty or whitespace-only
- **Examples**:
  - ✅ Valid: `"New Title"`, `"  Spaced  "` (becomes `"Spaced"`), omitted (None)
  - ❌ Invalid: `""`, `"   "`, `"\t\n"`

**description** (optional, keyword-only)
- **Type**: `str | None`
- **Default**: `None` (not updated)
- **Validation**: None (any value accepted)
- **Special Behavior**: Can be set to `None` to explicitly clear description
- **Examples**:
  - ✅ Valid: `"New description"`, `""` (empty string), `None` (clears), omitted (None)
  - All string values are valid

### Constraints

**C1: At Least One Field Required**
- At least one of `title` or `description` must be provided (not both None/omitted)
- Error: ValueError("No fields to update") if both omitted
- Rationale: Prevent no-op calls

**C2: Keyword-Only Parameters**
- `title` and `description` MUST be passed as keyword arguments
- Prevents: `update_task(1, "New Title", "New Desc")` ❌
- Requires: `update_task(1, title="New Title", description="New Desc")` ✅
- Rationale: Clarity and safety with optional parameters

---

## Output Contract

### Success Case

**Return Value**:
- **Type**: `dict[str, Any]`
- **Structure**:
  ```python
  {
      'id': int,               # Task ID (unchanged)
      'title': str,            # Current title (updated if provided)
      'description': str | None,  # Current description (updated if provided, can be None)
      'completed': bool,       # Completion status (unchanged)
      'created_at': datetime   # Creation timestamp (unchanged)
  }
  ```

**Console Output**:
```
✓ Task #{task_id} updated successfully
```

**Side Effects**:
- Task object in `_tasks` list is modified in-place
- Only specified fields (title and/or description) are updated
- All other fields (id, completed, created_at) remain unchanged

**Guarantees**:
1. Returned dictionary contains **all** task fields (not just updated ones)
2. Returned dictionary reflects current state after update
3. Immutable fields (id, completed, created_at) match pre-update values
4. Updated fields match input values (after normalization)

### Error Cases

**E1: No Fields Provided**
- **Condition**: Both `title` and `description` are None (or omitted)
- **Console Output**: `✗ Error: No fields to update`
- **Exception**: `ValueError("No fields to update")`
- **Side Effects**: None (storage unchanged)

**E2: Task Not Found**
- **Condition**: No task with ID `task_id` exists in storage
- **Console Output**: `✗ Error: Task #{task_id} not found`
- **Exception**: `ValueError(f"Task #{task_id} not found")`
- **Side Effects**: None (storage unchanged)

**E3: Empty Title**
- **Condition**: `title` parameter is empty or whitespace-only after stripping
- **Console Output**: `✗ Error: Task title cannot be empty`
- **Exception**: `ValueError("Task title cannot be empty")`
- **Side Effects**: None (storage unchanged)

**Error Handling Guarantees**:
1. All validations occur **before** any state changes (atomicity)
2. On any error, storage remains unchanged (no partial updates)
3. Error message is printed to stdout before exception is raised
4. Exception message matches console error message (without "✗ Error: " prefix)

---

## State Transitions

### Successful Update Flow

```
┌─────────────────────────────────────────────────────────┐
│ INITIAL STATE                                            │
│ _tasks = [Task(id=1, title="Old", description="Old")]  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                   update_task(1, title="New")
                          │
                          ▼
              ┌──────────────────────┐
              │ VALIDATION           │
              │ 1. Fields provided?  │ ✅ Yes (title)
              │ 2. Task exists?      │ ✅ Yes (id=1)
              │ 3. Title non-empty?  │ ✅ Yes ("New")
              └──────────────────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │ UPDATE               │
              │ task.title = "New"   │
              └──────────────────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │ OUTPUT               │
              │ Print: ✓ Task #1...  │
              │ Return: {...}        │
              └──────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ FINAL STATE                                              │
│ _tasks = [Task(id=1, title="New", description="Old")]  │
└─────────────────────────────────────────────────────────┘
```

### Error Flow (Task Not Found)

```
┌─────────────────────────────────────────────────────────┐
│ INITIAL STATE                                            │
│ _tasks = [Task(id=1, ...), Task(id=2, ...)]            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                   update_task(999, title="New")
                          │
                          ▼
              ┌──────────────────────┐
              │ VALIDATION           │
              │ 1. Fields provided?  │ ✅ Yes (title)
              │ 2. Task exists?      │ ❌ No (id=999 not found)
              └──────────────────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │ ERROR HANDLING       │
              │ Print: ✗ Error...    │
              │ Raise: ValueError    │
              └──────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ FINAL STATE (UNCHANGED)                                  │
│ _tasks = [Task(id=1, ...), Task(id=2, ...)]            │
└─────────────────────────────────────────────────────────┘
```

---

## Validation Order

**Critical**: Validations execute in this order (fail-fast):

1. **V1: At Least One Field Provided**
   - Check: `title is None and description is None`
   - Cost: O(1) - cheapest validation
   - Error: "No fields to update"

2. **V2: Task Exists**
   - Check: Linear search through `_tasks` for matching `task_id`
   - Cost: O(n) - requires storage lookup
   - Error: "Task #{task_id} not found"

3. **V3: Title Non-Empty (if provided)**
   - Check: `title.strip() != ""` if `title is not None`
   - Cost: O(m) where m = title length
   - Error: "Task title cannot be empty"

**Rationale**:
- Cheapest validation first (no fields check)
- Storage lookup second (more expensive)
- Field-specific validation last (only if field provided)
- Fail-fast: Stop at first error, don't continue validating

---

## Performance Characteristics

**Time Complexity**:
- Best case: O(1) - first validation fails (no fields)
- Average case: O(n) - task lookup where n = number of tasks
- Worst case: O(n + m) - task lookup + title validation where m = title length

**Space Complexity**: O(1) - in-place mutation, no additional structures

**Performance Targets** (from SC-006):
- **Target**: < 10ms per update operation
- **Expected**: < 1ms for typical task lists (< 100 tasks)
- **Scaling**: Linear with task count (acceptable for prototype)

---

## Compatibility

**Compatible Features**:
- ✅ 001-add-task: Creates tasks that update_task can modify
- ✅ 002-mark-complete: Preserves completion status during update
- ✅ 003-delete-task: No conflict (different operations)

**Incompatible Operations**:
- ❌ Cannot update `id` field (use delete + add instead)
- ❌ Cannot update `completed` field (use toggle_task_completion)
- ❌ Cannot update `created_at` field (immutable by design)

**Concurrent Operations**: N/A (single-threaded console application)

---

## Testing Contract

**Unit Test Coverage Required**:
1. ✅ Update title only (title changes, description preserved)
2. ✅ Update description only (description changes, title preserved)
3. ✅ Update both fields (both change, others preserved)
4. ✅ Clear description (set to None)
5. ✅ Immutable fields preserved (id, completed, created_at unchanged)
6. ✅ Whitespace stripping (title normalized)
7. ✅ Error: No fields provided
8. ✅ Error: Task not found
9. ✅ Error: Empty title
10. ✅ Return value structure (all fields present)
11. ✅ Console output (confirmation message)

**Integration Test Coverage Required**:
1. ✅ add_task → update_task flow
2. ✅ update_task → toggle_task_completion (fields preserved)
3. ✅ Multiple tasks updated independently

**Performance Test Coverage Required**:
1. ✅ Execution time < 10ms
2. ✅ Scaling with task count (acceptable degradation)

---

## Contract Summary

**Input**: task_id (int), optional title (str), optional description (str | None)
**Output**: Dictionary with all task fields OR ValueError
**Side Effect**: Prints confirmation/error message
**Guarantees**: Atomic updates, immutable field preservation, fail-fast validation
**Performance**: < 10ms (target), O(n) complexity
**Dependencies**: src.models.Task, src.storage._tasks

**Contract Version**: 1.0
**Status**: Defined (implementation pending)
