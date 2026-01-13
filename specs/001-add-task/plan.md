# Implementation Plan: Add Task

**Branch**: `001-add-task` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-add-task/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an in-memory task creation feature that allows users to add tasks with required titles and optional descriptions. The system assigns unique sequential IDs, validates input, provides user feedback, and stores tasks with timestamps. This is the foundational feature for the Todo application.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`dataclasses`, `datetime`)
**Storage**: In-memory (Python list) - no persistence
**Testing**: pytest (already configured in project)
**Target Platform**: Console application (Linux/Windows/macOS)
**Project Type**: Single project (console app)
**Performance Goals**: Instant task creation (<10ms for in-memory operations)
**Constraints**: No file I/O, no database, no external dependencies beyond stdlib
**Scale/Scope**: Single-user console application; expected <1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Specification-First Development
- **Status**: PASS
- **Evidence**: Complete spec exists at `specs/001-add-task/spec.md` with user stories, functional requirements, and acceptance criteria
- **Action**: None required

### ✅ Data Constraint: In-Memory Only
- **Status**: PASS
- **Evidence**: FR-006 explicitly requires in-memory storage without persistence
- **Action**: None required

### ✅ Quality Standards
- **Status**: PASS (to be enforced during implementation)
- **Requirements**:
  - PEP 8 compliance
  - Type hints for all functions (FR-005 specifies types)
  - Docstrings for public interfaces
  - Modular structure
- **Action**: Enforce during implementation phase

### ✅ No External Dependencies
- **Status**: PASS
- **Evidence**: Spec dependencies section lists only Python stdlib (`dataclasses`, `datetime`)
- **Action**: None required

### ✅ Development Workflow (SDD)
- **Status**: PASS
- **Evidence**: Following prescribed workflow (Spec → Plan → Tasks → Implementation)
- **Action**: Continue following workflow

**Gate Result**: ✅ ALL CHECKS PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-add-task/
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
├── models.py           # Task dataclass and related models
├── task_manager.py     # Task creation and management logic
├── storage.py          # In-memory storage management
└── __init__.py         # Package initialization

tests/
├── unit/
│   ├── test_task_model.py         # Task dataclass tests
│   ├── test_task_validation.py    # Input validation tests
│   └── test_task_creation.py      # Task creation logic tests
└── integration/
    └── test_add_task_flow.py      # End-to-end add task flow
```

**Structure Decision**: Single project structure selected. This is a console application with no separate frontend/backend or mobile components. The existing project already follows this pattern with `src/` and `tests/` directories.

**Existing Files to Modify**:
- `src/models.py` - Already exists; will define/update Task dataclass
- `src/task_manager.py` - Already exists; will implement add_task() function
- `src/storage.py` - Already exists; will manage in-memory task list

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied by this feature design.

---

## Phase 0: Research (Complete)

**Status**: ✅ Complete | **Document**: [research.md](./research.md)

### Key Technical Decisions

**1. Data Model: Python Dataclass**
- Selected `@dataclass` over plain class, NamedTuple, or dictionary
- Rationale: Native Python 3.13 feature with automatic `__init__`, `__repr__`, excellent IDE support
- See [ADR-0001](../../history/adr/0001-python-union-type-syntax-for-optional-values.md) for type hint decision

**2. ID Generation: Sequential Counter**
- Module-level counter with increment-before-assign pattern
- Rejected: UUID (not user-friendly), timestamp-based (collision risk), len(tasks)+1 (fragile)
- See [ADR-0003](../../history/adr/0003-sequential-counter-based-id-generation.md)

**3. Storage: In-Memory List**
- Module-level Python list for task storage
- Rejected: Dictionary (unnecessary complexity), singleton class (over-engineering), SQLite (violates constitution)
- See [ADR-0002](../../history/adr/0002-in-memory-list-storage-architecture.md)

**4. Validation Strategy**
- Fail-fast with ValueError for invalid title input
- Title validation: None, empty string, whitespace-only all rejected
- Description validation: None (accepts any string including empty)

**5. Return Value & User Feedback**
- Function returns task dictionary for programmatic access
- Prints confirmation message to console for user feedback
- Separation: function returns data, side effect prints message

### Performance Expectations

- Task creation: <10ms (in-memory list append is O(1) amortized)
- ID generation: O(1) counter increment
- Title validation: O(n) where n = title length for strip operation
- Expected scale: <1000 tasks per session (~500KB memory)

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
    completed: bool            # Defaults to False
    created_at: datetime       # Auto-generated UTC timestamp
```

**Invariants**:
1. `id` is unique and sequential (increments by 1)
2. `title` is never empty or None (enforced at creation)
3. `created_at` is set once and never modified
4. `completed` defaults to False for new tasks

**Storage Schema**:
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

**Module Organization**:
- `src/models.py` - Task dataclass definition
- `src/storage.py` - In-memory storage and ID generation
- `src/task_manager.py` - Business logic (add_task function)

**Quickstart Reference**: See [quickstart.md](./quickstart.md) for step-by-step TDD implementation guide with code examples.

---

## Phase 2: Implementation Tasks

**Status**: ✅ Complete | **Document**: [tasks.md](./tasks.md)

Tasks are organized by user story to enable independent implementation and testing:

- **Phase 1: Setup** (2 tasks) - Test infrastructure
- **Phase 2: Foundational** (3 tasks) - Core data model and storage (BLOCKS all user stories)
- **Phase 3: User Stories 1 & 3** (20 tasks) - MVP: Add basic task + validation
- **Phase 4: User Story 2** (7 tasks) - Enhancement: Add task with description
- **Phase 5: Polish** (8 tasks) - Coverage, edge cases, validation

**Total**: 40 tasks with 15+ parallel opportunities (37.5% parallelizable)

**MVP Milestone**: Complete phases 1-3 (25 tasks) for working task creation feature

See [tasks.md](./tasks.md) for detailed task breakdown with file paths, dependencies, and TDD checkpoints.

---

## Implementation Strategy

### Recommended Approach: MVP First 🎯

1. **Foundation First** (Phases 1-2): Setup infrastructure and core data model
2. **MVP Release** (Phase 3): Implement US1+US3 (basic task + validation)
   - STOP and VALIDATE: Run all tests, manual testing, verify acceptance criteria
   - **Deploy v1.0**: Working task creation with validation
3. **Enhancement Release** (Phase 4): Implement US2 (task with description)
   - Test independently, verify acceptance criteria
   - **Deploy v1.1**: Full feature with description support
4. **Polish** (Phase 5): Coverage, edge cases, final validation

### TDD Checkpoints (Mandatory)

After EVERY phase:
- **RED**: Run `pytest tests/` - Tests should FAIL (before implementation)
- **GREEN**: Run `pytest tests/` - Tests should PASS (after implementation)
- **REFACTOR**: Run `pytest tests/` - Tests should STILL PASS (after cleanup)

Do NOT proceed to next phase until all tests pass.

---

## Success Criteria

All criteria from [spec.md](./spec.md#success-criteria) must be met:

- ✅ **SC-001**: Users can add task with title only (single operation, immediate confirmation)
- ✅ **SC-002**: Sequential IDs assigned without collisions
- ✅ **SC-003**: 100% valid task creations succeed with confirmation
- ✅ **SC-004**: 100% invalid task creations rejected with error message
- ✅ **SC-005**: Optional descriptions captured with any string content
- ✅ **SC-006**: Timestamps accurate to the second

**Validation**: See tasks.md Phase 5 (T038-T039) for acceptance criteria validation tasks.

---

## Risk Assessment

### Low-Risk Decisions
- In-memory storage (mandated by constitution, well-understood)
- Python dataclass (standard pattern, good tooling)
- Sequential IDs (simple, deterministic, testable)

### Mitigated Risks
- **ID collision**: Counter guarantees uniqueness in single-threaded environment
- **Performance**: O(1) operations at expected scale (<1000 tasks)
- **Data loss**: Documented behavior (in-memory only, data lost on restart)

### Assumptions to Monitor
- Single-threaded operation (A3 in spec.md)
- No concurrent task creation
- Task volume stays below 1000 per session
- No persistence requirements in this phase

If any assumption is violated, revisit design decisions and update ADRs accordingly.

---

## Next Steps

1. ✅ Planning complete (all phases documented)
2. ✅ ADRs created for architectural decisions
3. → **Ready for implementation**: Run `/sp.implement` to begin TDD workflow
4. → Follow tasks.md sequentially (respect phase dependencies)
5. → Validate at each checkpoint (RED-GREEN-REFACTOR)

**Expected Timeline**: 40 tasks, MVP in 25 tasks (Phases 1-3)

