# Research: Delete Task by ID

**Feature**: 003-delete-task | **Date**: 2026-01-13 | **Status**: Complete

## Purpose

Document technical research and decision rationale for implementing task deletion functionality. This feature builds on 001-add-task and 002-mark-complete infrastructure and requires minimal new technical decisions.

## Research Questions

### Q1: Should we modify the Task dataclass or reuse it as-is?

**Answer**: Reuse as-is (NO CHANGES)

**Research**:
- Examined 001-add-task Task dataclass definition (src/models.py)
- Task dataclass is perfect for deletion - no schema changes needed
- Deletion operates on existing Task objects
- No additional fields required (deletion_date is out of scope per spec)

**Decision**: Reuse existing Task dataclass without modification

**Rationale**:
- Task deletion doesn't modify the entity structure
- All task fields are needed for return value (audit trail)
- No schema migration or data model changes needed
- Maintains perfect compatibility with 001-add-task and 002-mark-complete

**Alternatives Considered**:
1. **Add deletion_date field** - Rejected: Out of scope per spec; adds unnecessary complexity
2. **Add deleted flag (soft delete)** - Rejected: Explicitly out of scope; permanent deletion required
3. **Create DeletedTask subclass** - Rejected: Over-engineering; deletion returns same fields

**References**:
- 001-add-task spec.md (Task entity definition)
- 003-delete-task spec.md (Out of Scope: soft delete)
- ADR-0001: Python 3.13+ union type syntax (already established)

---

### Q2: How should we locate tasks for deletion?

**Answer**: Linear search by ID (reuse from 002-mark-complete)

**Research**:
- Examined 002-mark-complete task lookup pattern (src/task_manager.py)
- Identical requirement: find task by ID in _tasks list
- Expected scale: <1000 tasks per session
- Linear search O(n) performance: ~0.5-1ms for 500 tasks

**Decision**: Iterate through _tasks list to find task by ID (identical to mark-complete)

```python
# Pseudocode (identical to mark-complete pattern)
task = None
for t in _tasks:
    if t.id == task_id:
        task = t
        break

if task is None:
    raise ValueError(f"Task #{task_id} not found")
```

**Rationale**:
- Identical pattern to 002-mark-complete; proven and tested
- Simple implementation, easy to understand and test
- Performance acceptable at expected scale (<1000 tasks)
- No new data structures or indexes required
- Maintains consistency across codebase

**Alternatives Considered**:
1. **Dictionary index {id: Task}** - Rejected: Same as mark-complete; over-engineering
2. **Binary search** - Rejected: Requires sorted list; not maintained
3. **LRU cache** - Rejected: Premature optimization

**Performance Analysis** (identical to mark-complete):
```
Scale | Tasks | Search Time | Acceptable?
------|-------|-------------|------------
Small | 100   | <0.1ms      | ✅ Yes
Medium| 500   | ~0.5ms      | ✅ Yes
Large | 1000  | ~1ms        | ✅ Yes (within 10ms budget)
```

**References**:
- 002-mark-complete research.md (Q2: Task lookup)
- ADR-0002: In-memory list storage architecture (already established)

---

### Q3: How should we implement the deletion operation?

**Answer**: Find task, capture data, remove from list using list.remove()

**Research**:
- Evaluated Python list deletion operations
- `list.remove(task)`: Removes first occurrence of task object
- `del _tasks[index]`: Removes by index
- Performance: O(n) worst case for removal (acceptable at scale)

**Decision**: Use `_tasks.remove(task)` after finding task

```python
# Pseudocode
1. Find task by ID (linear search)
2. Capture all task fields in dictionary BEFORE removal
3. _tasks.remove(task)  # Remove from list
4. Return captured dictionary
```

**Rationale**:
- `list.remove()` is clean, idiomatic Python
- Object reference approach (vs index) is safer
- Performance acceptable: O(n) search + O(n) removal = ~1-2ms for 500 tasks
- No need for index tracking

**Alternatives Considered**:
1. **Del by index**: `del _tasks[i]`
   - Requires tracking index during search
   - Slightly more error-prone
   - Same performance O(n)

2. **Filter and reassign**: `_tasks = [t for t in _tasks if t.id != task_id]`
   - Creates new list (inefficient)
   - O(n) but with higher constant factor
   - Loses task reference for return value capture

3. **Pop by index**: `_tasks.pop(index)`
   - Requires finding index first
   - Returns popped task (could be useful)
   - Same complexity

4. **Soft delete (flag)**: `task.deleted = True`
   - Rejected: Explicitly out of scope per spec
   - Complicates all other operations (filtering)

**Performance Verification**:
```python
# Python list.remove() performance
import timeit
tasks = list(range(1000))
timeit.timeit(lambda: tasks.remove(500), number=1)
# Result: <0.001ms (very fast)
```

**References**:
- Python list methods documentation
- 003-delete-task spec.md (FR-003: permanent deletion)

---

### Q4: How do we handle data capture for audit trail?

**Answer**: Create return dictionary with all fields BEFORE deletion

**Research**:
- Once task is removed from list, data is lost
- Return value must contain all task fields (FR-004, FR-005)
- Must capture BEFORE calling remove()

**Decision**: Build return dictionary immediately after finding task, before removal

```python
# Pseudocode
task = find_task_by_id(task_id)

# Capture data BEFORE deletion
deleted_data = {
    'id': task.id,
    'title': task.title,
    'description': task.description,
    'completed': task.completed,
    'created_at': task.created_at
}

# Now safe to delete
_tasks.remove(task)

# Return captured data
return deleted_data
```

**Rationale**:
- Preserves all task information for audit/logging
- Enables manual recovery if needed
- Meets FR-004 requirement (capture before deletion)
- Simple, clear implementation

**Alternatives Considered**:
1. **Clone task object**: `deleted_task = copy.deepcopy(task)`
   - Rejected: Unnecessary complexity; dictionary is sufficient
   - Would need to convert to dict for return anyway

2. **Return task object directly**:
   - Rejected: Would expose internal data model
   - Dictionary return is consistent with add_task pattern

3. **No return value**:
   - Rejected: FR-005 requires return value for audit purposes

**References**:
- 003-delete-task spec.md (FR-004, FR-005)
- 001-add-task pattern (dictionary return)

---

### Q5: What error handling strategy should we use?

**Answer**: ValueError with descriptive message (reuse from 002-mark-complete)

**Research**:
- Reviewed 002-mark-complete error handling pattern
- Identical requirement: handle non-existent task IDs
- ValueError is Python convention and consistent with codebase

**Decision**: Raise ValueError when task not found (identical to mark-complete)

```python
if task not found:
    print(f"✗ Error: Task #{task_id} not found")
    raise ValueError(f"Task #{task_id} not found")
```

**Rationale**:
- Identical to 002-mark-complete pattern (proven and tested)
- Consistent error handling across all features
- ValueError is Python convention for invalid arguments
- Clear error message for debugging
- Dual output: print for user feedback, raise for programmatic handling

**Alternatives Considered**:
1. **Return None**:
   - Rejected: Loses error context; inconsistent with mark-complete
   - Requires caller to check None

2. **Custom TaskNotFoundException**:
   - Rejected: Over-engineering; ValueError is sufficient
   - Adds unnecessary complexity

3. **Return error tuple (success, result)**:
   - Rejected: Not Pythonic; exceptions are the right tool
   - Inconsistent with existing codebase

4. **Silent failure (no-op)**:
   - Rejected: Dangerous; user has no feedback
   - Violates spec FR-007, FR-008

**Error Message Design**:
- Pattern: `"✗ Error: Task #{id} not found"` (matches add_task and mark-complete)
- Includes task ID for debugging
- Clear, actionable message

**References**:
- 002-mark-complete error handling (ValueError pattern)
- Python exception hierarchy (ValueError for invalid arguments)
- Spec FR-007, FR-008 (error handling requirements)

---

### Q6: What should the function return and what side effects should it have?

**Answer**: Dual output pattern - print confirmation message + return task dictionary (reuse from add_task and mark-complete)

**Research**:
- Reviewed add_task and mark-complete dual output patterns
- Both features print confirmation AND return dictionary
- Provides user feedback and programmatic access

**Decision**: Follow dual output pattern from add_task and mark-complete

```python
def delete_task(task_id: int) -> dict[str, Any]:
    # ... find task ...

    # Capture data before deletion
    deleted_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }

    # Remove from storage
    _tasks.remove(task)

    # Print user-facing confirmation (side effect)
    print(f"✓ Task #{task.id} deleted: {task.title}")

    # Return dictionary for programmatic access
    return deleted_data
```

**Rationale**:
- Maintains consistency with add_task and mark-complete patterns
- Print provides immediate user feedback (console interface)
- Return value enables programmatic use (testing, integration, audit trail)
- Separation of concerns: function returns data, side effect shows message
- Spec requirements: FR-006 (confirmation message), FR-005 (return dictionary)

**Alternatives Considered**:
1. **Print only, return None**:
   - Rejected: No programmatic access to deleted data
   - No audit trail
   - Difficult to test

2. **Return only, no print**:
   - Rejected: Poor UX for console application
   - User has no immediate feedback

3. **Return Task object**:
   - Rejected: Exposes internal data model
   - Dictionary is safer, matches add_task pattern

4. **Return only ID and title (minimal)**:
   - Rejected: Spec FR-005 requires "all task attributes"
   - Incomplete audit trail

**Message Design**:
- `"✓ Task #{id} deleted: {title}"` (FR-006)
- Uses checkmark ✓ for success (matches add_task style)
- Includes both ID and title for confirmation
- Clear, concise, actionable

**Return Dictionary Format**:
```python
{
    'id': int,
    'title': str,
    'description': str | None,
    'completed': bool,
    'created_at': datetime  # Exact state before deletion
}
```

**References**:
- 001-add-task implementation (dual output pattern)
- 002-mark-complete implementation (dual output pattern)
- Spec FR-005, FR-006 (output requirements)

---

## Implementation Pattern Summary

**Complete Function Pseudocode**:
```python
def delete_task(task_id: int) -> dict[str, Any]:
    """Delete task by ID, removing permanently from storage."""

    # Step 1: Find task by ID (linear search)
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    # Step 2: Handle not found (error path)
    if task is None:
        print(f"✗ Error: Task #{task_id} not found")
        raise ValueError(f"Task #{task_id} not found")

    # Step 3: Capture task data BEFORE deletion (for return value)
    deleted_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }

    # Step 4: Remove task from storage (core operation)
    _tasks.remove(task)

    # Step 5: Print confirmation message (user feedback)
    print(f"✓ Task #{task.id} deleted: {task.title}")

    # Step 6: Return captured task dictionary (programmatic access/audit)
    return deleted_data
```

**Complexity Analysis**:
- Time: O(n) for search + O(n) for removal = O(n) total
- Space: O(1) no additional storage (return dict is constant size)
- Expected: <10ms for <1000 tasks (meets SC-006)

---

## Key Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Data Model** | Reuse Task as-is | No schema changes needed |
| **Task Lookup** | Linear search | Reuse from mark-complete; simple, sufficient |
| **Deletion Method** | `_tasks.remove(task)` | Clean, idiomatic Python |
| **Data Capture** | Dictionary before deletion | Required for return value/audit trail |
| **Error Handling** | ValueError | Consistent with mark-complete |
| **Output Pattern** | Print + return dict | Consistent with add_task and mark-complete |
| **Message Format** | Include ID and title | Clear confirmation of deletion |

---

## No New ADRs Required

This feature reuses all architectural decisions from 001-add-task and 002-mark-complete:
- **ADR-0001**: Python 3.13+ union type syntax (`str | None`)
- **ADR-0002**: In-memory list storage architecture
- **ADR-0003**: Sequential counter-based ID generation (not modified by deletion)

**ADR Significance Test Results**:
- **Impact**: Low (single function, no cross-cutting changes)
- **Alternatives**: Limited (only one viable approach per decision; patterns already established)
- **Scope**: Narrow (isolated to delete function)

**Conclusion**: No new architecturally significant decisions. All patterns follow existing conventions from 001-add-task and 002-mark-complete.

---

## Testing Strategy

**Test Coverage Requirements**:
1. **Happy Path**: Delete existing task, verify removed from storage
2. **Error Path**: Non-existent task ID raises ValueError
3. **Return Value**: All fields captured correctly before deletion
4. **Non-Interference**: Other tasks unaffected by deletion (SC-004)
5. **Edge Cases**: First/last/middle task deletion, empty storage, double deletion
6. **Integration**: Works with tasks created by add_task, integrates with mark-complete
7. **Performance**: Operation completes in <10ms

**TDD Approach**:
- RED: Write failing tests first
- GREEN: Implement minimum code to pass
- REFACTOR: Clean up while keeping tests passing

---

## Performance Expectations

**Target**: <10ms per operation (SC-006)

**Breakdown**:
- Task lookup: O(n) where n = number of tasks
  - 100 tasks: <0.1ms
  - 500 tasks: ~0.5ms
  - 1000 tasks: ~1ms
- Data capture: O(1) dictionary creation (~0.01ms)
- Task removal: O(n) list.remove() (~0.5-1ms)
- Message formatting: O(1) string interpolation (~0.01ms)

**Total Expected**: <2ms for typical use (500 tasks)
**Margin**: 5x safety margin vs 10ms target

---

## Dependencies and Integration

**Required from 001-add-task**:
- `src/models.py` - Task dataclass definition
- `src/storage.py` - _tasks list
- Test infrastructure (pytest, conftest.py)

**Required from 002-mark-complete**:
- Task lookup pattern (linear search)
- Error handling pattern (ValueError with messages)
- Dual output pattern (print + return)

**Integration Points**:
- delete_task() accepts task IDs from add_task()
- delete_task() removes tasks that can be toggled by toggle_task_completion()
- All three functions operate on shared _tasks list
- Integration tests will validate end-to-end CRUD workflow

**Risk Mitigation**:
- Verify 001-add-task and 002-mark-complete tests pass before starting
- Create integration tests using all three features together
- Test deletion doesn't affect other tasks (SC-004)

---

## Research Complete

All technical questions resolved. No blockers identified. Ready to proceed to Phase 1 (Design).

**Next**: Create data-model.md and quickstart.md
