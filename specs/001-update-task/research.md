# Research: Update Task Implementation

**Feature**: 001-update-task
**Date**: 2026-01-14
**Purpose**: Document validation strategy, field update patterns, and error handling approach

---

## RQ-001: Validation Strategy

**Question**: What validation order ensures clear, specific error messages?

**Context**: The spec requires 3 distinct error messages (FR-011, FR-012, FR-013):
- FR-011: "✗ Error: Task #{id} not found" when task ID doesn't exist
- FR-012: "✗ Error: Task title cannot be empty" when title is empty/whitespace
- FR-013: "✗ Error: No fields to update" when no update fields provided

**Research Analysis**:

Examined existing features for validation patterns:
- **001-add-task**: Validates title before creating task (fail-fast at earliest point)
- **002-mark-complete**: Validates task existence first, then performs operation
- **003-delete-task**: Validates task existence before deletion

**Decision**: Validate in this order:
1. **Fields provided check** (FR-013) - earliest validation, no storage lookup needed
2. **Task existence check** (FR-011) - second, requires storage lookup
3. **Title validation** (FR-012) - last, only if title provided

**Rationale**:
- Fail-fast principle: cheapest validation first
- User experience: "no fields" error more actionable than "task not found" when both conditions true
- Consistency: matches pattern from other features (validate inputs → validate state → perform action)

**Alternatives Considered**:
- ❌ Task existence first: Would require storage lookup even when no fields provided
- ❌ Title validation first: Would fail on empty title before checking if task exists
- ✅ **Chosen**: Fields → Existence → Title (progressive validation from cheap to expensive)

---

## RQ-002: Field Update Pattern

**Question**: How to update only specified fields while preserving others?

**Context**: Both title and description are optional parameters, but at least one must be provided (FR-004). Need to update only specified fields while preserving id, completed, created_at (FR-007).

**Research Analysis**:

**Pattern Options**:
1. **In-place mutation**: Modify task object directly
2. **Replace entire object**: Create new Task instance
3. **Copy-on-write**: Clone task, modify, replace in list

**Existing Feature Patterns**:
- **002-mark-complete**: Uses in-place mutation (`task.completed = not task.completed`)
- **Task dataclass**: Mutable by default (no `frozen=True`)

**Decision**: Use in-place mutation pattern

**Implementation**:
```python
# Find task
task = next((t for t in _tasks if t.id == task_id), None)

# Update only provided fields
if title is not None:
    task.title = title.strip()
if description is not None:  # Note: Can be None to clear
    task.description = description
```

**Rationale**:
- Consistency with 002-mark-complete pattern
- Efficient: No object creation overhead
- Clear intent: Explicit field assignments
- Preserves immutable fields automatically (id, completed, created_at not touched)

**Alternatives Considered**:
- ❌ Replace object: Would require recreating created_at, error-prone
- ❌ Copy-on-write: Over-engineering for in-memory list
- ✅ **Chosen**: In-place mutation (matches existing codebase patterns)

---

## RQ-003: Whitespace Handling

**Question**: Should title whitespace stripping match add_task behavior?

**Context**: FR-015 requires stripping leading/trailing whitespace from title. add_task already implements this.

**Research Analysis**:

**add_task Implementation** (from src/task_manager.py:50-56):
```python
# Validate title
if title is None or not title.strip():
    print("✗ Error: Task title cannot be empty")
    raise ValueError("Task title cannot be empty")

# Store stripped title
title = title.strip()
```

**Decision**: Reuse exact validation pattern from add_task

**Implementation**:
```python
if title is not None:
    title_stripped = title.strip()
    if not title_stripped:
        print("✗ Error: Task title cannot be empty")
        raise ValueError("Task title cannot be empty")
    task.title = title_stripped
```

**Rationale**:
- **Consistency**: Same behavior across add_task and update_task
- **Spec alignment**: FR-012 error message matches add_task exactly
- **User expectation**: Users expect same validation rules for create and update
- **Code reuse**: Same validation logic, same error messages

**Differences from add_task**:
- add_task: `title` is required parameter, checks for None
- update_task: `title` is optional, only validate if provided

**Alternatives Considered**:
- ❌ Different validation: Would confuse users (why different rules?)
- ❌ Skip stripping: Would allow whitespace-only titles in updates
- ✅ **Chosen**: Match add_task validation exactly (when title provided)

---

## Best Practices: Python Keyword-Only Parameters

**Context**: Function signature uses keyword-only parameters (`*` separator)

**Pattern**:
```python
def update_task(task_id: int, *, title: str | None = None, description: str | None = None):
```

**Benefits**:
1. **Clarity**: Forces callers to name parameters: `update_task(1, title="New")`
2. **Safety**: Prevents positional argument confusion: `update_task(1, "New", "Desc")` → ERROR
3. **Future-proof**: Can add parameters without breaking calls
4. **Self-documenting**: Code reads as `update_task(task_id, title="...")`, clear intent

**Consistency**: This pattern is **new** to the codebase (add_task, toggle_task_completion, delete_task use positional)

**Rationale for Using Here**:
- Multiple optional parameters with same type (str | None)
- Risk of confusion: `update_task(1, "New", None)` vs `update_task(1, None, "New")`
- Spec assumption documents this signature explicitly
- Best practice for Python 3.8+ optional parameters

---

## API Return Value: Dictionary Structure

**Context**: FR-010 requires returning dictionary with all task attributes

**Pattern** (from add_task, toggle_task_completion):
```python
return {
    'id': task.id,
    'title': task.title,
    'description': task.description,
    'completed': task.completed,
    'created_at': task.created_at
}
```

**Decision**: Return dictionary with **all** task fields (not just updated ones)

**Rationale**:
- **Consistency**: Matches add_task and toggle_task_completion return format
- **User convenience**: Caller gets complete task state without additional lookup
- **Immutability verification**: Tests can verify id/completed/created_at unchanged
- **Spec requirement**: FR-010 explicitly requires "all task attributes"

**Alternative** (not chosen):
- Return only updated fields: Would break pattern, require separate get_task call

---

## Error Handling: ValueError Pattern

**Context**: All validation errors raise ValueError (FR-014)

**Existing Pattern** (from add_task, toggle_task_completion, delete_task):
```python
print("✗ Error: [specific message]")
raise ValueError("[specific message]")
```

**Decision**: Follow dual output pattern for all errors:
1. Print error message to stdout
2. Raise ValueError with same message

**Rationale**:
- **Consistency**: All features use this pattern
- **User experience**: Error visible in console immediately
- **Testability**: Tests can capture stdout and verify exception
- **Debugging**: Error visible even if exception caught

**Error Message Format**:
- Prefix: "✗ Error: " (consistent with existing features)
- Specificity: Include task ID in "not found" message (FR-011)
- Clarity: Message describes what's wrong and how to fix it

---

## Performance Considerations

**Target**: < 10ms per update operation (SC-006)

**Current Implementation Analysis**:
- Task lookup: O(n) linear search through `_tasks` list
- Field updates: O(1) direct assignment
- Validation: O(1) string operations

**Estimated Performance**:
- Small task lists (< 100): Well under 1ms
- Large task lists (1000+): ~1-2ms (Python list iteration is fast)
- **Conclusion**: Linear search acceptable for prototype/MVP

**Optimization Opportunities** (not needed now):
- Use dictionary for O(1) lookup: `_tasks_by_id = {t.id: t for t in _tasks}`
- Trade-off: Memory overhead, additional maintenance

**Decision**: Keep linear search (matches existing features)

**Rationale**:
- Consistency with add_task, toggle_task_completion, delete_task
- Performance target easily met with current approach
- YAGNI: Don't optimize prematurely
- Can optimize later if profiling shows need

---

## Test Structure

**Files to Create**:
1. `tests/unit/test_update_task.py`: Core update tests (US1, US2)
2. `tests/unit/test_update_edge_cases.py`: Edge cases from spec
3. `tests/integration/test_update_task_flow.py`: Integration with add_task

**Test Organization** (following 002-mark-complete pattern):
```python
# tests/unit/test_update_task.py
class TestUpdateTaskUS1:  # Core update functionality
class TestUpdateTaskUS2:  # Error handling
class TestUpdateTaskOutput:  # Return value validation

# tests/unit/test_update_edge_cases.py
class TestUpdateEdgeCases:  # Special characters, long titles, rapid updates
class TestUpdatePerformance:  # < 10ms validation

# tests/integration/test_update_task_flow.py
class TestUpdateTaskIntegration:  # add_task → update_task flows
```

**Fixture Reuse**:
- `reset_task_storage` (from conftest.py): Reset between tests
- Follow pytest conventions from existing tests

---

## Summary

**Key Decisions**:
1. **Validation Order**: Fields → Existence → Title (fail-fast, cheap to expensive)
2. **Update Pattern**: In-place mutation (matches existing features)
3. **Whitespace Handling**: Match add_task validation exactly
4. **Keyword-Only Parameters**: Use for clarity and safety with optional params
5. **Return Value**: Dictionary with all task fields (consistency)
6. **Error Handling**: Dual output (print + raise) with specific messages
7. **Performance**: Linear search acceptable (< 10ms easily achieved)
8. **Test Structure**: 3 files following 002-mark-complete pattern

**No NEEDS CLARIFICATION Items Remaining**: All design questions resolved through analysis of existing features and spec requirements.

**Next Phase**: Generate data-model.md, contracts/, and quickstart.md (Phase 1)
