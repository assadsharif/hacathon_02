# Implementation Plan: Update Task Details

**Branch**: `001-update-task` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-update-task/spec.md`

## Summary

Implement `update_task()` function to allow users to modify existing task title and/or description. The function validates inputs, updates only specified fields while preserving immutable fields (id, completed, created_at), provides clear error messages, and follows the dual output pattern (console message + return value) established in 001-add-task. This extends the existing in-memory task management system with selective field update capability.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (dataclasses, datetime)
**Storage**: In-memory (Python list) - reuses existing `_tasks` from 001-add-task
**Testing**: pytest (inherited from project setup)
**Target Platform**: Local development (console/CLI interface)
**Project Type**: Single project (console application)
**Performance Goals**: < 10ms per update operation
**Constraints**: In-memory only (no persistence), single-user, no concurrency
**Scale/Scope**: Prototype/MVP - extends 3 existing Phase I features (001-add-task, 002-mark-complete, 003-delete-task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Compliance (Section I)

✅ **READ ONLY**: Phase I specs remain untouched
- This is a Phase I feature extending the console application
- Location: `specs/001-update-task/` (follows Phase I naming)
- Builds on existing foundation without modifying prior features

✅ **Authority Order**:
- Follows 001-add-task specification as reference behavior
- Reuses Task dataclass, storage layer, and validation patterns
- Maintains consistency with dual output pattern

### Technology Lock (Section II)

✅ **Phase I Stack Compliance**:
- Language: Python 3.13+ ✓
- Storage: In-memory (module-level `_tasks` list) ✓
- Interface: Console/CLI (function-level) ✓

✅ **No New Dependencies**:
- Reuses existing dataclasses, datetime
- No external packages required

### Spec-Driven Development (Section III)

✅ **Workflow Compliance**:
- Specification created (`specs/001-update-task/spec.md`) ✓
- Planning in progress (this document) ✓
- Tasks generation pending (`/sp.tasks`) ✓
- Implementation blocked until specs approved ✓

✅ **No Anti-Patterns**:
- No vibe coding - all behavior specified
- No inline architecture decisions
- Following `/sp.*` workflow
- No unplanned refactors

### Test-First Development (Section IV)

✅ **TDD Commitment**:
- RED phase: Write tests first (unit + integration)
- GREEN phase: Implement to pass tests
- REFACTOR phase: Clean up while maintaining pass
- User approval of tests before implementation

✅ **Coverage Plan**:
- Unit tests: All 15 functional requirements
- Edge cases: 7 scenarios identified in spec
- Integration tests: Integration with add_task workflow
- Performance tests: Validate < 10ms constraint

### Behavioral Compatibility (Section V)

✅ **Phase I Extension**:
- Extends existing Task entity (no schema changes)
- Preserves add_task, toggle_task_completion, delete_task behavior
- Follows established patterns (validation, error handling, dual output)
- Deterministic behavior (same input → same output)

### Simplicity and Focus (Section VI)

✅ **Explicit Non-Goals Respected**:
- No AI features ✓
- No real-time sync ✓
- No background jobs ✓
- No UI polish ✓
- YAGNI: Only implements specified update functionality ✓

✅ **Constraints Honored**:
- Smallest viable change: Single function addition
- No unrelated refactors
- One feature at a time

### Observability (Section VII)

✅ **Observability Plan**:
- Clear error messages per spec (FR-011, FR-012, FR-013)
- Confirmation messages for successful updates (FR-009)
- Structured error handling with ValueError
- Console output for debugging

**GATE STATUS**: ✅ **PASSED** - No constitution violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-update-task/
├── spec.md              # Feature specification (COMPLETE)
├── checklists/
│   └── requirements.md  # Spec quality validation (COMPLETE)
├── plan.md              # This file (/sp.plan output - IN PROGRESS)
├── research.md          # Phase 0 output (PENDING)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── contracts/           # Phase 1 output (PENDING)
└── tasks.md             # Phase 2 output (/sp.tasks - PENDING)
```

### Source Code (repository root)

```text
src/
├── models.py           # Task dataclass (EXISTING - no changes needed)
├── storage.py          # _tasks list, _generate_task_id (EXISTING - no changes needed)
└── task_manager.py     # ADD: update_task() function (NEW)

tests/
├── conftest.py         # reset_task_storage fixture (EXISTING - reuse)
├── unit/
│   ├── test_toggle_completion.py      # (EXISTING - 002-mark-complete)
│   ├── test_toggle_edge_cases.py      # (EXISTING - 002-mark-complete)
│   ├── test_update_task.py            # NEW: Core update tests
│   └── test_update_edge_cases.py      # NEW: Edge case tests
└── integration/
    ├── test_toggle_completion_flow.py # (EXISTING - 002-mark-complete)
    └── test_update_task_flow.py       # NEW: Integration with add_task
```

**Structure Decision**: Single project structure maintained. This feature extends the existing console application by adding one new function to `src/task_manager.py` and corresponding test files. No changes to data models or storage layer required - complete reuse of 001-add-task infrastructure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations identified.** This feature fully complies with all constitution principles.

---

## Phase 0: Research & Analysis

### Research Questions

**RQ-001: Validation Strategy**
- **Question**: What validation order ensures clear, specific error messages?
- **Context**: Spec requires 3 distinct error messages (FR-011, FR-012, FR-013)
- **Research Focus**: Validate in order of: (1) task existence, (2) field presence, (3) title non-empty

**RQ-002: Field Update Pattern**
- **Question**: How to update only specified fields while preserving others?
- **Context**: title and description are optional; at least one required (FR-004)
- **Research Focus**: Pattern: Check which fields provided → validate → update in place

**RQ-003: Whitespace Handling**
- **Question**: Should title whitespace stripping match add_task behavior?
- **Context**: FR-015 requires stripping; add_task already implements this
- **Research Focus**: Reuse add_task validation logic for consistency

### Investigation Plan

1. **Review Existing Patterns** (001-add-task, 002-mark-complete, 003-delete-task):
   - Error handling patterns
   - Validation order
   - Dual output implementation
   - Test structure and fixtures

2. **Design Validation Flow**:
   - Define validation sequence
   - Map error conditions to error messages
   - Ensure atomicity (all validations before any updates)

3. **API Design Verification**:
   - Confirm function signature from spec
   - Validate keyword-only parameters approach
   - Design return dictionary structure

### Expected Outcomes

- **research.md**: Documents validation strategy, field update pattern, and error handling approach
- **Decision Log**: Records choices made and alternatives considered
- **Best Practices**: Captures Python idioms for optional parameters and selective updates

---

## Phase 1: Design & Contracts

### Data Model Analysis

**Existing Entity: Task** (from 001-add-task)
```python
@dataclass
class Task:
    id: int                    # IMMUTABLE
    title: str                 # MUTABLE via update_task
    description: str | None    # MUTABLE via update_task
    completed: bool            # IMMUTABLE (use toggle_task_completion)
    created_at: datetime       # IMMUTABLE
```

**Field Update Semantics**:
- **Mutable**: `title`, `description`
- **Immutable**: `id`, `completed`, `created_at`
- **Validation**: title must be non-empty string (after strip), description can be None

**No schema changes required** - reuses existing Task dataclass from `src/models.py`.

### API Contract

**Function Signature**:
```python
_UNSET = object()  # Sentinel to distinguish "not provided" from "explicitly None"

def update_task(
    task_id: int,
    *,
    title: str | _UNSET = _UNSET,
    description: str | None | _UNSET = _UNSET
) -> dict[str, Any]:
    """Update an existing task's title and/or description."""
```

**Contract Details**:

**Input Contract**:
- `task_id` (int, required): Task identifier to update
- `title` (str | None, keyword-only, optional): New title (must be non-empty if provided)
- `description` (str | None, keyword-only, optional): New description (can be None to clear)
- **Constraint**: At least one of `title` or `description` must be provided

**Output Contract**:
- **Success**: Returns `dict[str, Any]` with all task fields (id, title, description, completed, created_at)
- **Failure**: Raises `ValueError` with specific error message

**Side Effects**:
- Prints confirmation message to stdout: `"✓ Task #{id} updated successfully"`
- Modifies task in `_tasks` list in place

**Error Conditions**:
| Condition | Error Message | Exception |
|-----------|---------------|-----------|
| Task ID not found | `"✗ Error: Task #{id} not found"` | ValueError |
| No fields provided | `"✗ Error: No fields to update"` | ValueError |
| Empty title provided | `"✗ Error: Task title cannot be empty"` | ValueError |

**Validation Order** (fail-fast):
1. Check at least one field provided
2. Check task exists
3. Validate title (if provided) is non-empty after strip

**State Transition**:
```
BEFORE: Task(id=1, title="Old", description="Old desc", completed=False, created_at=T1)
ACTION: update_task(1, title="New")
AFTER:  Task(id=1, title="New", description="Old desc", completed=False, created_at=T1)
```

### Integration Points

**Dependencies**:
- `src.models.Task`: Task dataclass (read-only dependency)
- `src.storage._tasks`: In-memory task list (read-write dependency)
- `src.storage._generate_task_id`: ID generator (no dependency - not used)

**Integration with Existing Features**:
- **001-add-task**: Creates tasks that update_task can modify
- **002-mark-complete**: Completion status preserved during update
- **003-delete-task**: No conflict (different operations)

**Test Integration**:
- Reuse `reset_task_storage` fixture from `tests/conftest.py`
- Follow test structure from 002-mark-complete
- Integrate with add_task in integration tests

### Quickstart Guide

**File**: `specs/001-update-task/quickstart.md`

**Contents**:
1. **Usage Examples**: Basic title update, description update, both fields update
2. **Error Handling**: Examples of each error condition
3. **Integration**: Using with add_task and toggle_task_completion
4. **Testing**: How to run unit and integration tests

---

## Phase 2: Task Breakdown (Next Command)

**Command**: `/sp.tasks`

**Expected Output**: `specs/001-update-task/tasks.md`

**Task Structure**:
- **Phase 1: Setup** (T001-T005): Prerequisites, branch verification
- **Phase 2: RED - Unit Tests** (T006-T025): Write failing tests for all 15 FRs
- **Phase 3: RED - Integration Tests** (T026-T030): Write failing integration tests
- **Phase 4: GREEN - Implementation** (T031-T035): Implement update_task to pass tests
- **Phase 5: REFACTOR** (T036-T040): Clean up, optimize, document
- **Phase 6: Validation** (T041-T050): Coverage, performance, spec compliance

**Estimated Task Count**: ~50 tasks (following 002-mark-complete pattern)

---

## Implementation Strategy

### Validation Logic

```python
_UNSET = object()  # Sentinel to distinguish "not provided" from "explicitly None"

def update_task(
    task_id: int,
    *,
    title: str | _UNSET = _UNSET,
    description: str | None | _UNSET = _UNSET
) -> dict[str, Any]:
    """Update an existing task's title and/or description."""
    # 1. Validate at least one field provided
    if title is _UNSET and description is _UNSET:
        print("✗ Error: No fields to update")
        raise ValueError("No fields to update")

    # 2. Find task by ID
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    if task is None:
        print(f"✗ Error: Task #{task_id} not found")
        raise ValueError(f"Task #{task_id} not found")

    # 3. Validate and update title if provided
    if title is not _UNSET:
        title_stripped = title.strip()
        if not title_stripped:
            print("✗ Error: Task title cannot be empty")
            raise ValueError("Task title cannot be empty")
        task.title = title_stripped

    # 4. Update description if provided (can be None to clear)
    if description is not _UNSET:
        task.description = description  # Accepts None to clear

    # 5. Print confirmation and return
    print(f"✓ Task #{task_id} updated successfully")
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }
```

### Testing Strategy

**Unit Tests** (`tests/unit/test_update_task.py`):
- US1: Core update functionality (title only, description only, both)
- US2: Error handling (non-existent ID, empty title, no fields)
- Field preservation tests (immutable fields unchanged)
- Whitespace handling tests

**Edge Case Tests** (`tests/unit/test_update_edge_cases.py`):
- Long titles (1000+ characters)
- Special characters (emojis, unicode)
- Description set to None (clearing)
- Rapid successive updates

**Integration Tests** (`tests/integration/test_update_task_flow.py`):
- add_task → update_task flow
- update_task → toggle_task_completion flow
- Multiple tasks updated independently

**Performance Tests**:
- Measure execution time (target: < 10ms)
- Test with multiple tasks in storage

### Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| Inconsistent validation with add_task | Reuse same whitespace stripping and empty check logic |
| Immutable fields accidentally modified | Explicit preservation in implementation; tests verify |
| Error message inconsistency | Follow exact messages from spec; tests verify exact text |
| Performance regression | Include performance test in validation phase |

---

## Success Criteria Validation

All 6 success criteria from spec will be validated:

- **SC-001**: Single function call updates → Unit tests verify
- **SC-002**: Selective field updates → Tests verify only specified fields change
- **SC-003**: Description clearing → Test with description=None
- **SC-004**: Empty title rejection → Tests verify error message and ValueError
- **SC-005**: Non-existent ID handling → Tests verify error handling
- **SC-006**: Performance < 10ms → Performance test measures execution time

---

## Next Steps

1. ✅ **Constitution Check**: PASSED - no violations
2. 🔄 **Phase 0**: Generate `research.md` (validation patterns, field update strategy)
3. ⏳ **Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md`
4. ⏳ **Phase 2**: Run `/sp.tasks` to generate task breakdown
5. ⏳ **Implementation**: Execute TDD workflow (RED-GREEN-REFACTOR)

**Current Status**: Planning complete. Ready for Phase 0 research generation.
