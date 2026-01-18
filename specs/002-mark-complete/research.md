# Research: Toggle Task Completion

**Feature**: 002-mark-complete | **Date**: 2026-01-13 | **Status**: Complete

## Purpose

Document technical research and decision rationale for implementing task completion toggle functionality. This feature builds on 001-add-task infrastructure and requires minimal new technical decisions.

## Research Questions

### Q1: Should we modify the Task dataclass or reuse it as-is?

**Answer**: Reuse as-is (NO CHANGES)

**Research**:
- Examined 001-add-task Task dataclass definition (src/models.py)
- Task already includes `completed: bool` field (defaults to False)
- Field is mutable and designed for modification
- No additional fields required per spec (completion_date is out of scope)

**Decision**: Reuse existing Task dataclass without modification

**Rationale**:
- Task.completed field already exists and supports toggle operation
- No schema migration or data model changes needed
- Minimizes risk and complexity
- Maintains perfect compatibility with 001-add-task

**Alternatives Considered**:
1. **Add completion_date field** - Rejected: Out of scope per spec; adds unnecessary complexity
2. **Create new CompletedTask subclass** - Rejected: Over-engineering; single field toggle doesn't warrant inheritance
3. **Use separate completed_tasks list** - Rejected: Complicates storage, violates single source of truth

**References**:
- 001-add-task spec.md (Task entity definition)
- ADR-0001: Python 3.13+ union type syntax (already established)

---

### Q2: How should we locate tasks in the _tasks list?

**Answer**: Linear search by ID

**Research**:
- Examined 001-add-task storage architecture (src/storage.py)
- Storage is a flat Python list: `_tasks: list[Task] = []`
- Expected scale: <1000 tasks per session
- Linear search O(n) performance: ~0.5ms for 500 tasks

**Decision**: Iterate through _tasks list to find task by ID

```python
# Pseudocode
for task in _tasks:
    if task.id == task_id:
        return task
raise ValueError(f"Task #{task_id} not found")
```

**Rationale**:
- Simple implementation, easy to understand and test
- Performance acceptable at expected scale (<1000 tasks)
- No new data structures or indexes required
- Consistent with existing codebase patterns

**Alternatives Considered**:
1. **Dictionary index {id: Task}** - Rejected: Over-engineering; adds complexity without meaningful benefit at scale
2. **Binary search** - Rejected: Requires sorted list; IDs are sequential but not guaranteed sorted in storage order
3. **LRU cache for recent lookups** - Rejected: Premature optimization; no evidence of repeated lookups
4. **Generator expression with next()** - Considered: More Pythonic but equivalent complexity; linear search is clearer

**Performance Analysis**:
```
Scale | Tasks | Search Time | Acceptable?
------|-------|-------------|------------
Small | 100   | <0.1ms      | ✅ Yes
Medium| 500   | ~0.5ms      | ✅ Yes
Large | 1000  | ~1ms        | ✅ Yes (within 10ms budget)
XL    | 5000  | ~5ms        | ⚠️ Marginal (but out of scope)
```

**References**:
- ADR-0002: In-memory list storage architecture (already established)
- Python list iteration performance (O(n) with low constant factor)

---

### Q3: How should we implement the toggle operation?

**Answer**: Direct boolean negation (`task.completed = not task.completed`)

**Research**:
- Evaluated toggle patterns in Python
- Boolean negation is idiomatic and atomic
- Tested in Python 3.13 REPL: `not True == False`, `not False == True`

**Decision**: Use direct boolean negation

```python
task.completed = not task.completed
```

**Rationale**:
- Single operation, clear semantics
- Idiomatic Python
- Atomic update (no race conditions in single-threaded environment)
- Self-documenting code

**Alternatives Considered**:
1. **Explicit if/else**:
   ```python
   if task.completed:
       task.completed = False
   else:
       task.completed = True
   ```
   - Rejected: Verbose, no benefit over negation

2. **XOR flip**: `task.completed ^= True`
   - Rejected: Less readable, obscure for boolean toggle

3. **Setter method**: `task.set_completed(not task.completed)`
   - Rejected: Dataclass doesn't use setters; violates Python idioms

4. **State machine** (Complete/Incomplete states):
   - Rejected: Over-engineering for binary toggle

**Verification**:
```python
# Tested in Python 3.13
>>> completed = False
>>> completed = not completed
>>> completed
True
>>> completed = not completed
>>> completed
False
```

**References**:
- Python boolean operations documentation
- PEP 8 style guide (prefer simple expressions)

---

### Q4: What error handling strategy should we use for invalid task IDs?

**Answer**: Raise ValueError with descriptive message

**Research**:
- Reviewed 001-add-task error handling patterns
- add_task() raises ValueError for invalid title input
- Python convention: ValueError for invalid function arguments

**Decision**: Raise ValueError when task not found

```python
if task not found:
    print(f"✗ Error: Task #{task_id} not found")
    raise ValueError(f"Task #{task_id} not found")
```

**Rationale**:
- Consistent with add_task() validation pattern
- ValueError is Python convention for invalid arguments
- Clear error message for debugging
- Dual output: print for user feedback, raise for programmatic handling

**Alternatives Considered**:
1. **Return None**:
   - Rejected: Loses error context; requires caller to check None
   - Inconsistent with add_task() behavior

2. **Custom TaskNotFoundException**:
   - Rejected: Over-engineering; ValueError is sufficient
   - Adds unnecessary complexity (new exception class)

3. **Return error tuple (success, result)**:
   - Rejected: Not Pythonic; exceptions are the right tool
   - Complicates caller code

4. **Silent failure (no-op)**:
   - Rejected: Dangerous; user has no feedback
   - Violates spec FR-008, FR-009

**Error Message Design**:
- Pattern: `"✗ Error: Task #{id} not found"` (matches add_task error style)
- Includes task ID for debugging
- Clear, actionable message

**References**:
- 001-add-task error handling (ValueError for validation)
- Python exception hierarchy (ValueError for invalid arguments)
- Spec FR-008, FR-009 (error handling requirements)

---

### Q5: What should the function return and what side effects should it have?

**Answer**: Dual output pattern - print confirmation message + return task dictionary

**Research**:
- Reviewed 001-add-task dual output pattern
- add_task() prints confirmation AND returns dictionary
- Provides both user feedback and programmatic access

**Decision**: Follow dual output pattern from add_task()

```python
def toggle_task_completion(task_id: int) -> dict[str, Any]:
    # ... find and toggle task ...

    # Print user-facing confirmation (side effect)
    if task.completed:
        print(f"✓ Task #{task.id} marked as complete")
    else:
        print(f"✓ Task #{task.id} marked as incomplete")

    # Return dictionary for programmatic access
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }
```

**Rationale**:
- Maintains consistency with add_task() pattern
- Print provides immediate user feedback (console interface)
- Return value enables programmatic use (testing, integration)
- Separation of concerns: function returns data, side effect shows message
- Spec requirements: FR-004, FR-005 (messages), FR-006 (return dictionary)

**Alternatives Considered**:
1. **Print only, return None**:
   - Rejected: No programmatic access to result
   - Difficult to test, can't chain operations

2. **Return only, no print**:
   - Rejected: Poor UX for console application
   - User has no immediate feedback

3. **Return Task object**:
   - Rejected: Exposes internal data model
   - Dictionary is safer, matches add_task() pattern

4. **Return only changed fields (id, completed)**:
   - Rejected: Inconsistent with add_task() which returns full dictionary
   - Spec FR-006 requires "all task attributes"

**Message Design**:
- `"✓ Task #{id} marked as complete"` when False→True (FR-004)
- `"✓ Task #{id} marked as incomplete"` when True→False (FR-005)
- Uses checkmark ✓ for success (matches add_task style)
- Clear, concise, actionable

**Return Dictionary Format**:
```python
{
    'id': int,
    'title': str,
    'description': str | None,
    'completed': bool,  # ← New status after toggle
    'created_at': datetime
}
```

**References**:
- 001-add-task implementation (dual output pattern)
- Spec FR-004, FR-005, FR-006 (output requirements)

---

## Implementation Pattern Summary

**Complete Function Pseudocode**:
```python
def toggle_task_completion(task_id: int) -> dict[str, Any]:
    """Toggle task completion status between True and False."""

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

    # Step 3: Toggle completed field (core logic)
    task.completed = not task.completed

    # Step 4: Print status-appropriate message (user feedback)
    if task.completed:
        print(f"✓ Task #{task.id} marked as complete")
    else:
        print(f"✓ Task #{task.id} marked as incomplete")

    # Step 5: Return full task dictionary (programmatic access)
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }
```

**Complexity Analysis**:
- Time: O(n) for search + O(1) for toggle = O(n) total
- Space: O(1) no additional storage
- Expected: <10ms for <1000 tasks (meets SC-006)

---

## Key Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Data Model** | Reuse Task as-is | completed field already exists |
| **Task Lookup** | Linear search | Simple, sufficient at scale |
| **Toggle Logic** | `not task.completed` | Idiomatic, atomic, clear |
| **Error Handling** | ValueError | Consistent with add_task |
| **Output Pattern** | Print + return dict | Consistent with add_task |
| **Message Format** | Status-based | Clear user feedback |

---

## No New ADRs Required

This feature reuses all architectural decisions from 001-add-task:
- **ADR-0001**: Python 3.13+ union type syntax (`str | None`)
- **ADR-0002**: In-memory list storage architecture
- **ADR-0003**: Sequential counter-based ID generation (not modified)

**ADR Significance Test Results**:
- **Impact**: Low (single function, no cross-cutting changes)
- **Alternatives**: Limited (only one viable approach per decision)
- **Scope**: Narrow (isolated to toggle function)

**Conclusion**: No new architecturally significant decisions. All patterns follow existing conventions.

---

## Testing Strategy

**Test Coverage Requirements**:
1. **Happy Path**: Toggle False→True and True→False
2. **Error Path**: Non-existent task ID raises ValueError
3. **Field Preservation**: Only completed changes, others unchanged
4. **Edge Cases**: Rapid toggles, empty storage, invalid IDs
5. **Integration**: Works with tasks created by add_task()
6. **Performance**: Operation completes in <10ms

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
- Toggle operation: O(1) boolean negation (~0.001ms)
- Message formatting: O(1) string interpolation (~0.01ms)
- Dictionary creation: O(1) constant fields (~0.01ms)

**Total Expected**: <2ms for typical use (500 tasks)
**Margin**: 5x safety margin vs 10ms target

---

## Dependencies and Integration

**Required from 001-add-task**:
- `src/models.py` - Task dataclass definition
- `src/storage.py` - _tasks list
- Test infrastructure (pytest, conftest.py)

**Integration Points**:
- toggle_task_completion() accepts task IDs from add_task()
- Both functions operate on shared _tasks list
- Integration tests will validate end-to-end workflow

**Risk Mitigation**:
- Verify 001-add-task tests pass before starting
- Create integration tests using both features together
- Document assumptions about 001-add-task stability

---

## Research Complete

All technical questions resolved. No blockers identified. Ready to proceed to Phase 1 (Design).

**Next**: Create data-model.md and quickstart.md
