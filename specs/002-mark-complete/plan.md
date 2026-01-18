# Implementation Plan: Toggle Task Completion

**Branch**: `002-mark-complete` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-mark-complete/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a task completion toggle feature that allows users to mark tasks as complete or incomplete by toggling a boolean field. The system validates task existence, updates the completed status bidirectionally (False↔True), preserves all other task fields, provides status-appropriate user feedback, and returns the updated task dictionary. This feature builds directly on the 001-add-task foundation.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`dataclasses`, `datetime`) - inherited from 001-add-task
**Storage**: In-memory (Python list) - reuses existing `_tasks` from 001-add-task
**Testing**: pytest (already configured in project)
**Target Platform**: Console application (Linux/Windows/macOS)
**Project Type**: Single project (console app)
**Performance Goals**: Instant toggle operation (<10ms for in-memory list search + update)
**Constraints**: No file I/O, no database, no external dependencies beyond stdlib
**Scale/Scope**: Single-user console application; operates on existing task list from 001-add-task

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Specification-First Development
- **Status**: PASS
- **Evidence**: Complete spec exists at `specs/002-mark-complete/spec.md` with 2 prioritized user stories, 10 functional requirements, and 6 success criteria with validation methods
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
specs/002-mark-complete/
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
├── task_manager.py     # NEW: toggle_task_completion() function
├── storage.py          # In-memory storage (NO CHANGES - reuses 001-add-task)
└── __init__.py         # Package initialization

tests/
├── unit/
│   ├── test_toggle_completion.py      # Toggle logic and validation tests
│   └── test_toggle_edge_cases.py      # Edge cases: rapid toggles, field preservation
└── integration/
    └── test_toggle_completion_flow.py # End-to-end toggle flow with add_task integration
```

**Structure Decision**: Single project structure maintained from 001-add-task. This feature extends the existing console application without introducing new architectural layers.

**Existing Files to Modify**:
- `src/task_manager.py` - Add new `toggle_task_completion()` function alongside existing `add_task()`

**Existing Files Reused (No Changes)**:
- `src/models.py` - Task dataclass already has `completed` field
- `src/storage.py` - `_tasks` list and search capability already exist

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied by this feature design. Feature intentionally minimizes complexity by reusing all existing infrastructure from 001-add-task.

---

## Phase 0: Research (Complete)

**Status**: ✅ Complete | **Document**: [research.md](./research.md)

### Key Technical Decisions

**1. No New Data Model Required**
- Decision: Reuse existing Task dataclass from 001-add-task without modification
- Rationale: Task already has `completed: bool` field (defaults to False)
- Alternatives considered: Add completion_date field (rejected - out of scope per spec)

**2. Task Lookup Strategy: Linear Search**
- Decision: Iterate through `_tasks` list to find task by ID
- Rationale: Simple, sufficient for scale (<1000 tasks), no new infrastructure
- Alternatives considered: Dictionary index (over-engineering), binary search (requires sorted list)

**3. Toggle Implementation: Direct Negation**
- Decision: `task.completed = not task.completed`
- Rationale: Single operation, clear semantics, atomic update
- Alternatives considered: Explicit if/else (verbose), state machine (over-engineering)

**4. Error Handling: ValueError with Descriptive Message**
- Decision: Raise ValueError when task ID not found (FR-009)
- Rationale: Consistent with add_task validation pattern, clear error contract
- Alternatives considered: Return None (loses error context), custom exception (unnecessary)

**5. Dual Output Pattern: Console + Return Dictionary**
- Decision: Print confirmation message + return full task dictionary (FR-004, FR-005, FR-006)
- Rationale: Maintains consistency with add_task pattern (established in ADR for 001-add-task)
- Alternatives considered: Print-only (no programmatic access), return-only (poor UX)

### Performance Expectations

- Task lookup: O(n) where n = number of tasks (~500 tasks avg → <1ms)
- Toggle operation: O(1) boolean negation
- Total operation: <10ms target (SC-006)
- Expected scale: <1000 tasks per session (inherited from 001-add-task)

### No New ADRs Required

All architectural decisions reuse patterns from 001-add-task:
- **ADR-0001**: Python 3.13+ union type syntax (str | None)
- **ADR-0002**: In-memory list storage architecture
- **ADR-0003**: Sequential counter-based ID generation (not modified)

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
    completed: bool            # ⚡ MODIFIED BY THIS FEATURE: Toggled False↔True
    created_at: datetime       # Auto-generated UTC timestamp
```

**Field Modification**:
- `completed` field is the ONLY field modified by toggle_task_completion()
- All other fields (id, title, description, created_at) are IMMUTABLE during toggle (FR-007)

**Invariants** (inherited from 001-add-task):
1. `id` is unique and sequential
2. `title` is never empty or None
3. `created_at` is set once and never modified
4. `completed` can toggle between True and False freely

**Storage Schema** (unchanged from 001-add-task):
- `_tasks: list[Task] = []` - Ordered by creation time
- `_task_id_counter: int = 0` - Increments before assignment

### Implementation Approach

**TDD Workflow** (mandated by constitution):
```
RED → GREEN → REFACTOR
```

1. **RED**: Write tests first, ensure they fail
2. **GREEN**: Implement minimum code to pass tests
3. **REFACTOR**: Clean up code while keeping tests passing

**Function Signature** (from spec FR-001, FR-006):
```python
def toggle_task_completion(task_id: int) -> dict[str, Any]:
    """
    Toggle a task's completion status between True and False.

    Args:
        task_id: The ID of the task to toggle

    Returns:
        Dictionary with all task fields (id, title, description, completed, created_at)

    Raises:
        ValueError: If task with given ID does not exist

    Side Effects:
        Prints confirmation message indicating new completion status:
        - "✓ Task #{id} marked as complete" (when toggled False→True)
        - "✓ Task #{id} marked as incomplete" (when toggled True→False)
    """
```

**Module Organization**:
- `src/models.py` - Task dataclass (NO CHANGES)
- `src/storage.py` - In-memory storage (NO CHANGES)
- `src/task_manager.py` - NEW FUNCTION: toggle_task_completion()

**Algorithm**:
```python
1. Search _tasks list for task with matching ID
2. If not found: print error, raise ValueError (FR-008, FR-009)
3. If found: toggle completed field (FR-003)
4. Print appropriate message based on NEW status (FR-004, FR-005)
5. Return task dictionary (FR-006)
```

**Quickstart Reference**: See [quickstart.md](./quickstart.md) for step-by-step TDD implementation guide with code examples.

---

## Phase 2: Implementation Tasks

**Status**: PENDING | **Document**: tasks.md (generated by `/sp.tasks` command)

Tasks will be organized by user story to enable independent implementation and testing:

- **Phase 1: Setup** (~2 tasks) - Test infrastructure (may already exist from 001-add-task)
- **Phase 2: Foundational** (~1 task) - Import existing infrastructure
- **Phase 3: User Story 1 (P1)** (~12-15 tasks) - Core toggle functionality
- **Phase 4: User Story 2 (P2)** (~5-7 tasks) - Error handling for invalid IDs
- **Phase 5: Polish** (~5-7 tasks) - Edge cases, performance, validation

**Estimated Total**: ~25-32 tasks (40% fewer than 001-add-task due to infrastructure reuse)

**MVP Milestone**: Complete phases 1-4 for full feature implementation

See tasks.md (generated by `/sp.tasks`) for detailed task breakdown with file paths, dependencies, and TDD checkpoints.

---

## Implementation Strategy

### Recommended Approach: Incremental Build on 001-add-task 🎯

1. **Foundation Verification** (Phase 1-2): Verify 001-add-task infrastructure intact
2. **Core Toggle** (Phase 3): Implement US1 (basic toggle with confirmation messages)
   - STOP and VALIDATE: Run all tests, manual testing, verify bidirectional toggle
   - Test both directions: False→True and True→False
3. **Error Handling** (Phase 4): Implement US2 (invalid ID handling)
   - Test independently with various invalid scenarios
4. **Polish** (Phase 5): Edge cases, performance validation, final acceptance

### TDD Checkpoints (Mandatory)

After EVERY phase:
- **RED**: Run `pytest tests/` - Tests should FAIL (before implementation)
- **GREEN**: Run `pytest tests/` - Tests should PASS (after implementation)
- **REFACTOR**: Run `pytest tests/` - Tests should STILL PASS (after cleanup)

Do NOT proceed to next phase until all tests pass.

### Integration Testing with 001-add-task

**Critical**: Tests must demonstrate integration:
```python
# Example integration test pattern
task_dict = add_task("Test task")         # From 001-add-task
task_id = task_dict['id']
result = toggle_task_completion(task_id)  # From 002-mark-complete
assert result['completed'] == True
```

This validates that both features work together as a cohesive system.

---

## Success Criteria

All criteria from [spec.md](./spec.md#success-criteria) must be met:

- ✅ **SC-001**: Users can toggle any existing task's completion status in a single function call
- ✅ **SC-002**: System correctly toggles completion status bidirectionally (False→True and True→False)
- ✅ **SC-003**: System displays appropriate confirmation message based on new completion status
- ✅ **SC-004**: All non-completion task fields remain unchanged after toggle operation
- ✅ **SC-005**: System handles non-existent task IDs gracefully with clear error messages
- ✅ **SC-006**: Toggle operation completes in under 10ms for typical use cases

**Validation**: Tasks.md Phase 5 will include acceptance criteria validation tasks for all SC items.

---

## Risk Assessment

### Low-Risk Decisions
- Reuse existing Task dataclass (no schema changes, no migration risk)
- Linear search for task lookup (simple, deterministic, testable)
- Direct boolean negation for toggle (atomic, no race conditions)

### Mitigated Risks
- **Task not found**: Clear error handling with ValueError (FR-009, SC-005)
- **Performance**: O(n) search acceptable at scale (<1000 tasks → <1ms)
- **Field preservation**: Explicit testing to ensure only completed field changes (FR-007, SC-004)

### Integration Risks (Managed)
- **Dependency on 001-add-task**: Integration tests will validate both features work together
- **Storage state consistency**: Reusing existing _tasks list ensures no state divergence
- **Type compatibility**: Using existing Task dataclass ensures perfect compatibility

### Assumptions to Monitor
- Single-threaded operation (inherited from 001-add-task)
- No concurrent task modifications
- Task volume stays below 1000 per session
- 001-add-task infrastructure remains stable (no breaking changes)

If any assumption is violated, revisit design decisions.

---

## Dependencies

### Feature Dependencies
- **BLOCKS**: None
- **BLOCKED BY**: 001-add-task (REQUIRED - must be complete and committed)

### Technical Dependencies
- **Required Files** (from 001-add-task):
  - `src/models.py` - Task dataclass with completed field
  - `src/storage.py` - _tasks list for task storage
  - Tests infrastructure (pytest, conftest.py)

### Risk Mitigation
- Verify 001-add-task implementation before starting
- Run 001-add-task tests to ensure foundation is stable
- Create integration tests that use both features

---

## Next Steps

1. ✅ Planning complete (Phases 0-1 documented)
2. ✅ No new ADRs needed (reuses existing architecture)
3. → **Generate tasks**: Run `/sp.tasks` to create detailed task breakdown
4. → **Verify foundation**: Ensure 001-add-task tests pass before starting
5. → **Ready for implementation**: Run `/sp.implement` to begin TDD workflow
6. → Follow tasks.md sequentially (respect phase dependencies)
7. → Validate at each checkpoint (RED-GREEN-REFACTOR)

**Expected Timeline**: ~25-32 tasks, simpler than 001-add-task due to infrastructure reuse

**Key Success Factor**: Integration testing demonstrating both add_task and toggle_task_completion work together seamlessly
