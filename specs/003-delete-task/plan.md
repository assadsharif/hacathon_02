# Implementation Plan: Delete Task by ID

**Branch**: `003-delete-task` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-delete-task/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a task deletion feature that allows users to remove tasks from storage permanently by ID. The system validates task existence, captures all task data before deletion, removes the task from the list, provides confirmation feedback, and returns the complete task dictionary for audit purposes. This feature builds directly on 001-add-task and 002-mark-complete foundations.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`dataclasses`, `datetime`) - inherited from 001-add-task
**Storage**: In-memory (Python list) - reuses existing `_tasks` from 001-add-task
**Testing**: pytest (already configured in project)
**Target Platform**: Console application (Linux/Windows/macOS)
**Project Type**: Single project (console app)
**Performance Goals**: Instant delete operation (<10ms for in-memory list search + removal)
**Constraints**: No file I/O, no database, no external dependencies beyond stdlib
**Scale/Scope**: Single-user console application; operates on existing task list from 001-add-task

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Specification-First Development
- **Status**: PASS
- **Evidence**: Complete spec exists at `specs/003-delete-task/spec.md` with 2 prioritized user stories, 10 functional requirements, and 6 success criteria with validation methods
- **Action**: None required

### ✅ Data Constraint: In-Memory Only
- **Status**: PASS
- **Evidence**: Feature reuses existing in-memory storage from 001-add-task; no new storage mechanism introduced
- **Action**: None required

### ✅ Quality Standards
- **Status**: PASS (to be enforced during implementation)
- **Requirements**:
  - PEP 8 compliance
  - Type hints for all functions (FR-001 specifies function signature with types)
  - Docstrings for public interfaces
  - Modular structure
- **Action**: Enforce during implementation phase

### ✅ No External Dependencies
- **Status**: PASS
- **Evidence**: Feature uses only Python stdlib; no new dependencies beyond 001-add-task
- **Action**: None required

### ✅ Development Workflow (SDD)
- **Status**: PASS
- **Evidence**: Following prescribed workflow (Spec → Plan → Tasks → Implementation)
- **Action**: Continue following workflow

### ✅ Test-First Development
- **Status**: PASS (to be enforced during implementation)
- **Evidence**: Spec defines clear acceptance scenarios; tasks will follow RED-GREEN-REFACTOR TDD cycle
- **Action**: All tests written before implementation, user approval before GREEN phase

**Gate Result**: ✅ ALL CHECKS PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/003-delete-task/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (PENDING)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── checklists/
│   └── requirements.md  # Spec validation checklist (COMPLETE)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models.py           # Task dataclass (NO CHANGES - reuses 001-add-task)
├── task_manager.py     # NEW: delete_task() function
├── storage.py          # In-memory storage (NO CHANGES - reuses 001-add-task)
└── __init__.py         # Package initialization

tests/
├── unit/
│   ├── test_delete_task.py           # Delete logic and validation tests
│   └── test_delete_edge_cases.py     # Edge cases: position deletions, storage effects
└── integration/
    └── test_delete_task_flow.py      # End-to-end delete flow with add_task integration
```

**Structure Decision**: Single project structure maintained from 001-add-task. This feature extends the existing console application without introducing new architectural layers.

**Existing Files to Modify**:
- `src/task_manager.py` - Add new `delete_task()` function alongside existing `add_task()` and `toggle_task_completion()`

**Existing Files Reused (No Changes)**:
- `src/models.py` - Task dataclass already defined
- `src/storage.py` - `_tasks` list and search capability already exist

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied by this feature design. Feature intentionally minimizes complexity by reusing all existing infrastructure from 001-add-task and patterns from 002-mark-complete.

---

## Phase 0: Research (Complete)

**Status**: ✅ Complete | **Document**: [research.md](./research.md)

### Key Technical Decisions

**1. No New Data Model Required**
- Decision: Reuse existing Task dataclass from 001-add-task without modification
- Rationale: Task deletion operates on existing Task objects
- Alternatives considered: Add deletion_date field (rejected - out of scope per spec)

**2. Task Lookup Strategy: Linear Search (Reuse from 002-mark-complete)**
- Decision: Iterate through `_tasks` list to find task by ID
- Rationale: Identical pattern to mark-complete; simple, sufficient for scale (<1000 tasks)
- Alternatives considered: Dictionary index (over-engineering), binary search (requires sorted list)

**3. Deletion Implementation: List.remove() with index search**
- Decision: Find task by ID, capture data, use `_tasks.remove(task)` or `del _tasks[index]`
- Rationale: Python list provides efficient removal operation
- Alternatives considered:
  - Filter and reassign (creates new list, inefficient)
  - Pop by index (requires finding index first, same complexity)
  - Mark as deleted flag (soft delete - explicitly out of scope)

**4. Data Capture Strategy: Store Before Deletion**
- Decision: Create return dictionary with all fields BEFORE calling remove()
- Rationale: Once removed, task data is lost; must capture for return value (FR-004, FR-005)
- Alternatives considered: Clone task object (unnecessary complexity)

**5. Error Handling: ValueError with Descriptive Message (Reuse from 002-mark-complete)**
- Decision: Raise ValueError when task ID not found (FR-008)
- Rationale: Identical to mark-complete pattern; consistent error handling
- Alternatives considered: Return None (loses error context), custom exception (unnecessary)

**6. Dual Output Pattern: Console + Return Dictionary (Reuse from 001-add-task and 002-mark-complete)**
- Decision: Print confirmation message + return full task dictionary (FR-006, FR-005)
- Rationale: Maintains consistency with add_task and mark-complete patterns
- Alternatives considered: Print-only (no audit trail), return-only (poor UX)

### Performance Expectations

- Task lookup: O(n) where n = number of tasks (~500 tasks avg → <1ms)
- Task removal: O(n) worst case for list.remove() (~500 tasks → <1ms)
- Total operation: <10ms target (SC-006)
- Expected scale: <1000 tasks per session (inherited from 001-add-task)

### No New ADRs Required

All architectural decisions reuse patterns from 001-add-task and 002-mark-complete:
- **ADR-0001**: Python 3.13+ union type syntax (str | None)
- **ADR-0002**: In-memory list storage architecture
- **ADR-0003**: Sequential counter-based ID generation (not modified by deletion)

No new architecturally significant decisions meet the ADR significance test (impact + alternatives + scope).

---

## Phase 1: Design (Complete)

**Status**: ✅ Complete | **Documents**: [data-model.md](./data-model.md), [quickstart.md](./quickstart.md)

### Data Model Design

**Task Entity** (see [data-model.md](./data-model.md#entities)):
```python
@dataclass
class Task:
    id: int                    # Unique sequential identifier (1, 2, 3...)
    title: str                 # Required, non-empty after strip
    description: str | None    # Optional, accepts any string or None
    completed: bool            # Task completion status
    created_at: datetime       # Auto-generated timestamp
```

**Operation**:
- Task is **REMOVED** from storage by delete_task()
- All fields are **CAPTURED** before removal for return dictionary

**Invariants** (inherited from 001-add-task):
1. `id` is unique and sequential
2. `title` is never empty or None
3. `created_at` is set once
4. Deletion does not affect other tasks in storage

**Storage Schema** (unchanged from 001-add-task):
- `_tasks: list[Task] = []` - Ordered by creation time
- `_task_id_counter: int = 0` - Increments before assignment (never decrements)

### Implementation Approach

**TDD Workflow** (mandated by constitution):
```
RED → GREEN → REFACTOR
```

1. **RED**: Write tests first, ensure they fail
2. **GREEN**: Implement minimum code to pass tests
3. **REFACTOR**: Clean up code while keeping tests passing

**Function Signature** (from spec FR-001, FR-005):
```python
def delete_task(task_id: int) -> dict[str, Any]:
    """
    Delete a task by its ID, removing it permanently from storage.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary with all task fields before deletion (id, title, description, completed, created_at)

    Raises:
        ValueError: If task with given ID does not exist

    Side Effects:
        Removes task from storage permanently (no undo)
        Prints confirmation message: "✓ Task #{id} deleted: {title}"
    """
```

**Module Organization**:
- `src/models.py` - Task dataclass (NO CHANGES)
- `src/storage.py` - In-memory storage (NO CHANGES)
- `src/task_manager.py` - NEW FUNCTION: delete_task()

**Algorithm**:
```python
1. Search _tasks list for task with matching ID
2. If not found: print error, raise ValueError (FR-007, FR-008)
3. If found: capture all task fields in dictionary (FR-004)
4. Remove task from _tasks list (FR-003)
5. Print confirmation message with task title (FR-006)
6. Return captured task dictionary (FR-005)
```

**Quickstart Reference**: See [quickstart.md](./quickstart.md) for step-by-step TDD implementation guide with code examples.

---

## Phase 2: Implementation Tasks

**Status**: PENDING | **Document**: tasks.md (generated by `/sp.tasks` command)

Tasks will be organized by user story to enable independent implementation and testing:

- **Phase 1: Setup** (~2 tasks) - Test infrastructure (may already exist from previous features)
- **Phase 2: Foundational** (~1 task) - Import existing infrastructure
- **Phase 3: User Story 1 (P1)** (~12-15 tasks) - Core delete functionality
- **Phase 4: User Story 2 (P2)** (~5-7 tasks) - Error handling for invalid IDs
- **Phase 5: Polish** (~5-7 tasks) - Edge cases, performance, validation

**Estimated Total**: ~25-30 tasks (similar to 002-mark-complete)

**MVP Milestone**: Complete phases 1-4 for full feature implementation

See tasks.md (generated by `/sp.tasks`) for detailed task breakdown with file paths, dependencies, and TDD checkpoints.

---

## Implementation Strategy

### Recommended Approach: Incremental Build on Existing Features 🎯

1. **Foundation Verification** (Phase 1-2): Verify 001-add-task and 002-mark-complete infrastructure intact
2. **Core Delete** (Phase 3): Implement US1 (basic delete with confirmation)
   - STOP and VALIDATE: Run all tests, manual testing, verify deletion and return value
   - Test deletion doesn't affect other tasks
3. **Error Handling** (Phase 4): Implement US2 (invalid ID handling)
   - Test independently with various invalid scenarios
4. **Polish** (Phase 5): Edge cases, performance validation, final acceptance

### TDD Checkpoints (Mandatory)

After EVERY phase:
- **RED**: Run `pytest tests/` - Tests should FAIL (before implementation)
- **GREEN**: Run `pytest tests/` - Tests should PASS (after implementation)
- **REFACTOR**: Run `pytest tests/` - Tests should STILL PASS (after cleanup)

Do NOT proceed to next phase until all tests pass.

### Integration Testing with Previous Features

**Critical**: Tests must demonstrate integration:
```python
# Example integration test pattern
task = add_task("Test task", "Description")  # From 001-add-task
task_id = task['id']
deleted = delete_task(task_id)  # From 003-delete-task
assert deleted['id'] == task_id
assert deleted['title'] == "Test task"
# Verify task no longer in storage
with pytest.raises(ValueError):
    delete_task(task_id)  # Should fail - already deleted
```

This validates that delete_task works with add_task and mark_complete infrastructure.

---

## Success Criteria

All criteria from [spec.md](./spec.md#success-criteria) must be met:

- ✅ **SC-001**: Users can delete any existing task by ID in a single function call
- ✅ **SC-002**: Deleted tasks are permanently removed from storage and cannot be retrieved
- ✅ **SC-003**: System returns complete task information before deletion for audit purposes
- ✅ **SC-004**: Deletion of one task does not affect other tasks in storage
- ✅ **SC-005**: System handles non-existent task IDs gracefully with clear error messages
- ✅ **SC-006**: Delete operation completes in under 10ms for typical use cases

**Validation**: Tasks.md Phase 5 will include acceptance criteria validation tasks for all SC items.

---

## Risk Assessment

### Low-Risk Decisions
- Reuse existing Task dataclass (no schema changes, no migration risk)
- Linear search for task lookup (simple, deterministic, testable) - same as mark-complete
- Python list.remove() for deletion (built-in, well-tested, efficient)

### Mitigated Risks
- **Task not found**: Clear error handling with ValueError (FR-008, SC-005)
- **Accidental deletion**: Return full task data for manual recovery if needed
- **Performance**: O(n) search + O(n) removal acceptable at scale (<1000 tasks → <2ms)
- **Storage corruption**: Test extensively to ensure only target task removed (SC-004)

### Integration Risks (Managed)
- **Dependency on 001-add-task**: Integration tests will validate both features work together
- **Dependency on 002-mark-complete**: Reusing task lookup and error handling patterns
- **Storage state consistency**: Removing from _tasks list ensures no state divergence
- **Type compatibility**: Using existing Task dataclass ensures perfect compatibility

### Assumptions to Monitor
- Single-threaded operation (inherited from 001-add-task)
- No concurrent task modifications
- Task volume stays below 1000 per session
- Previous features (001-add-task, 002-mark-complete) remain stable (no breaking changes)

If any assumption is violated, revisit design decisions.

---

## Dependencies

### Feature Dependencies
- **BLOCKS**: None
- **BLOCKED BY**:
  - 001-add-task (REQUIRED - must be complete and committed)
  - 002-mark-complete (RECOMMENDED - provides task lookup and error handling patterns)

### Technical Dependencies
- **Required Files** (from 001-add-task):
  - `src/models.py` - Task dataclass
  - `src/storage.py` - _tasks list for task storage
  - Tests infrastructure (pytest, conftest.py)
- **Required Patterns** (from 002-mark-complete):
  - Task lookup by ID (linear search)
  - Error handling (ValueError with messages)
  - Dual output (print + return)

### Risk Mitigation
- Verify 001-add-task implementation before starting
- Verify 002-mark-complete implementation for pattern consistency
- Run existing tests to ensure foundation is stable
- Create integration tests that use all three features together

---

## Next Steps

1. ✅ Planning complete (Phases 0-1 documented)
2. ✅ No new ADRs needed (reuses existing architecture and patterns)
3. → **Generate tasks**: Run `/sp.tasks` to create detailed task breakdown
4. → **Verify foundation**: Ensure 001-add-task and 002-mark-complete tests pass before starting
5. → **Ready for implementation**: Run `/sp.implement` to begin TDD workflow
6. → Follow tasks.md sequentially (respect phase dependencies)
7. → Validate at each checkpoint (RED-GREEN-REFACTOR)

**Expected Timeline**: ~25-30 tasks, similar complexity to 002-mark-complete due to infrastructure and pattern reuse

**Key Success Factor**: Integration testing demonstrating add_task, toggle_task_completion, and delete_task work together seamlessly to complete basic CRUD operations
