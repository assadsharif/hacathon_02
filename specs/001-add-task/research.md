# Research: Add Task Feature

**Feature**: Add Task (001-add-task)
**Date**: 2026-01-10
**Status**: Complete

## Overview

This document captures research findings and design decisions for the Add Task feature implementation. Since the feature requirements are straightforward and align with existing project patterns, no complex research was needed. All technical decisions are derived from the project constitution and feature specification.

## Technical Decisions

### 1. Data Model: Python Dataclass

**Decision**: Use Python `@dataclass` for the Task model

**Rationale**:
- Native Python 3.13 feature (no external dependencies)
- Automatic generation of `__init__`, `__repr__`, `__eq__` methods
- Clean syntax with type hints built-in
- Immutable field support if needed in future
- Excellent IDE support and type checking

**Alternatives Considered**:
1. **Plain Python class**
   - More verbose (manual `__init__` required)
   - No automatic equality comparison
   - Rejected: Unnecessary boilerplate

2. **NamedTuple**
   - Immutable by default
   - Rejected: Tasks may need mutation in future features (mark complete, update description)

3. **Dictionary**
   - No type safety
   - No IDE autocompletion
   - Rejected: Violates clean code principles

**Implementation**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
```

### 2. ID Generation Strategy

**Decision**: Module-level counter with increment-before-assign pattern

**Rationale**:
- Simplest approach for single-threaded in-memory application
- Sequential IDs are user-friendly and predictable
- No external dependencies required
- Meets FR-004 requirement for unique sequential IDs

**Alternatives Considered**:
1. **UUID**
   - Overkill for in-memory single-user app
   - Not user-friendly for display
   - Rejected: Doesn't meet "sequential" requirement

2. **Timestamp-based ID**
   - Risk of collisions if tasks created simultaneously
   - Not truly sequential
   - Rejected: Doesn't guarantee uniqueness in all scenarios

3. **len(tasks) + 1**
   - Breaks if tasks are deleted (out of scope but future consideration)
   - Can result in ID reuse
   - Rejected: Not robust for future extensibility

**Implementation Pattern**:
```python
_task_id_counter: int = 0

def _generate_task_id() -> int:
    global _task_id_counter
    _task_id_counter += 1
    return _task_id_counter
```

### 3. Storage: In-Memory List

**Decision**: Module-level list for task storage

**Rationale**:
- Satisfies constitution requirement: "All data must be stored IN-MEMORY only"
- Satisfies FR-006: "System MUST store tasks in memory without persistence"
- Simple, direct access pattern
- Sufficient for expected scale (<1000 tasks per session)

**Alternatives Considered**:
1. **Dictionary (id → task)**
   - Faster lookups by ID
   - Rejected for now: List iteration is fast enough at expected scale; dictionary adds complexity for no current benefit

2. **Class-based singleton storage**
   - More "object-oriented"
   - Rejected: Adds unnecessary abstraction for simple list management

**Implementation**:
```python
_tasks: list[Task] = []
```

### 4. Validation Strategy

**Decision**: Validate title at function entry, raise ValueError on failure

**Rationale**:
- Fail fast principle
- Clear error contract (documented in function signature via docstring)
- Satisfies FR-002, FR-008, FR-009
- Pythonic exception handling pattern

**Validation Rules** (from spec):
1. Title must not be None
2. Title must not be empty string after `.strip()`
3. Description can be None or any string (including empty)

**Implementation Pattern**:
```python
def add_task(title: str, description: str | None = None) -> dict[str, Any]:
    # Validate title
    if title is None or not title.strip():
        raise ValueError("Task title is required")

    # Proceed with task creation
    ...
```

### 5. Return Value & User Feedback

**Decision**: Return task as dictionary and print confirmation message

**Rationale**:
- Dictionary return enables programmatic access to created task
- Print confirmation satisfies FR-007 user feedback requirement
- Separation of concerns: function returns data, side effect prints message
- Testable: tests can verify return value without capturing stdout

**Message Format** (FR-007):
- Success: `"✓ Task #{id} added: {title}"`
- Error: `"✗ Error: Task title is required"`

## Best Practices Applied

### Python Standards
- **PEP 8**: All code follows Python style guide
- **Type Hints**: Full type annotations (`str | None` syntax for Optional)
- **Docstrings**: Google-style docstrings for all public functions
- **Error Messages**: Clear, actionable user feedback

### Testing Strategy
- **Unit Tests**: Test each component in isolation
  - Task model creation
  - ID generation
  - Validation logic
  - Storage operations
- **Integration Tests**: Test complete add_task flow end-to-end
- **Edge Cases**: Test boundary conditions (empty strings, whitespace, special characters)

### Code Organization
- **Separation of Concerns**:
  - `models.py`: Data structures (Task dataclass)
  - `storage.py`: Storage management (_tasks list, ID counter)
  - `task_manager.py`: Business logic (add_task function, validation)
- **Single Responsibility**: Each function/class has one clear purpose
- **DRY**: No code duplication

## Dependencies Summary

**Standard Library Only**:
- `dataclasses` - For Task model
- `datetime` - For timestamp generation
- `typing` - For type hints (built-in in Python 3.13)

**Testing**:
- `pytest` - Already configured in project
- No additional test dependencies needed

## Performance Considerations

**Expected Performance**:
- Task creation: <10ms (in-memory list append is O(1) amortized)
- ID generation: O(1) counter increment
- Title validation: O(n) where n = title length (strip operation)

**Scale Assumptions**:
- Expected: <1000 tasks per session
- Memory usage: ~1KB per task (negligible)
- No performance optimization needed at this scale

## Security & Validation

**Input Validation**:
- Title: Required, non-empty after whitespace stripping
- Description: Optional, accepts any string including empty
- No character limits imposed (per spec decision)

**Security Considerations**:
- Console application, single-user
- No user authentication required
- No SQL injection risk (no database)
- No XSS risk (no web interface)
- Input sanitization: Only whitespace stripping for title validation

## Open Questions

None. All technical decisions are resolved and documented above.

## Next Steps

1. ✅ Research complete
2. → Proceed to Phase 1: Create data-model.md
3. → Proceed to Phase 1: Create quickstart.md
4. → Update agent context with technology choices
5. → Run `/sp.tasks` to generate implementation tasks

