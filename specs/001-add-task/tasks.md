# Tasks: Add Task

**Input**: Design documents from `/specs/001-add-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: TDD workflow required per project constitution. All tests MUST be written FIRST and FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test structure

- [x] T001 Create test directory structure: tests/unit/ and tests/integration/
- [x] T002 [P] Create pytest fixture file tests/conftest.py for test state management

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and storage infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Define Task dataclass in src/models.py with attributes: id, title, description, completed, created_at
- [x] T004 [P] Implement in-memory storage infrastructure in src/storage.py: _tasks list and _task_id_counter
- [x] T005 Create ID generation function _generate_task_id() in src/storage.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 + 3 (Priority: P1) 🎯 MVP

**Combined Stories**:
- **US1**: Add Basic Task - Add task with title only
- **US3**: Handle Invalid Task Input - Validation and error handling

**Why Combined**: US3 (validation) is integral to US1 (basic task creation). Both are P1 and must be implemented together for a functioning MVP.

**Goal**: Users can add tasks with titles, receive confirmation, and get clear error messages for invalid input

**Independent Test**: Create a task with a valid title and verify ID assignment, storage, and confirmation message. Attempt to create tasks with invalid titles (empty, None, whitespace) and verify error messages and no task creation.

### Tests for User Story 1 + 3 (TDD - Write FIRST) ⚠️

> **CRITICAL: Write these tests FIRST, ensure they FAIL before implementation (RED phase)**

- [x] T006 [P] [US1] Write unit test for adding task with title only in tests/unit/test_add_task.py - test_add_task_with_title_only()
- [x] T007 [P] [US1] Write unit test for sequential ID generation in tests/unit/test_add_task.py - test_task_ids_are_sequential()
- [x] T008 [P] [US1] Write unit test for task storage in memory in tests/unit/test_add_task.py - test_task_stored_in_memory()
- [x] T009 [P] [US3] Write unit test for empty title validation in tests/unit/test_add_task.py - test_add_task_empty_title_raises_error()
- [x] T010 [P] [US3] Write unit test for None title validation in tests/unit/test_add_task.py - test_add_task_none_title_raises_error()
- [x] T011 [P] [US3] Write unit test for whitespace-only title validation in tests/unit/test_add_task.py - test_add_task_whitespace_title_raises_error()
- [x] T012 [P] [US1] Write integration test for complete add task flow in tests/integration/test_add_task_flow.py - test_add_basic_task_flow()

**Checkpoint (RED)**: Run `pytest tests/` - ALL tests should FAIL (code doesn't exist yet)

### Implementation for User Story 1 + 3 (GREEN phase)

- [x] T013 [US1] Implement add_task() function signature and docstring in src/task_manager.py
- [x] T014 [US3] Implement title validation logic in src/task_manager.py add_task() - check for None, empty, whitespace
- [x] T015 [US1] Implement ID generation call using _generate_task_id() in src/task_manager.py add_task()
- [x] T016 [US1] Implement timestamp generation using datetime.now() in src/task_manager.py add_task()
- [x] T017 [US1] Implement Task object creation in src/task_manager.py add_task()
- [x] T018 [US1] Implement task storage by appending to _tasks list in src/task_manager.py add_task()
- [x] T019 [US1] Implement success confirmation message print in src/task_manager.py add_task()
- [x] T020 [US3] Implement error message print for validation failure in src/task_manager.py add_task()
- [x] T021 [US1] Implement dictionary return value from add_task() in src/task_manager.py

**Checkpoint (GREEN)**: Run `pytest tests/` - ALL tests should PASS

### Refactoring for User Story 1 + 3 (REFACTOR phase)

- [x] T022 Review code for PEP 8 compliance in src/models.py, src/storage.py, src/task_manager.py
- [x] T023 Add type hints to all function signatures in src/task_manager.py and src/storage.py
- [x] T024 Add docstrings to all public functions in src/task_manager.py and src/storage.py
- [x] T025 Verify no code duplication between files

**Checkpoint (REFACTOR)**: Run `pytest tests/` - ALL tests should STILL PASS after refactoring

**Final Checkpoint**: At this point, User Stories 1 & 3 should be fully functional and testable independently. You have a working MVP!

---

## Phase 4: User Story 2 (Priority: P2)

**Goal**: Users can add tasks with both title AND description for richer task information

**Independent Test**: Create a task with title and description and verify both are stored. Create a task with empty string description and verify it's accepted.

**Builds On**: US1 (basic task creation) but enhances it with optional description parameter

### Tests for User Story 2 (TDD - Write FIRST) ⚠️

> **CRITICAL: Write these tests FIRST, ensure they FAIL before implementation (RED phase)**

- [x] T026 [P] [US2] Write unit test for adding task with title and description in tests/unit/test_add_task.py - test_add_task_with_description()
- [x] T027 [P] [US2] Write unit test for accepting empty string description in tests/unit/test_add_task.py - test_add_task_with_empty_description()
- [x] T028 [P] [US2] Write integration test for task with description flow in tests/integration/test_add_task_flow.py - test_add_task_with_description_flow()

**Checkpoint (RED)**: Run `pytest tests/unit/test_add_task.py::test_add_task_with_description -v` - Test should FAIL

### Implementation for User Story 2 (GREEN phase)

- [x] T029 [US2] Verify add_task() function already accepts optional description parameter in src/task_manager.py
- [x] T030 [US2] Verify Task dataclass already has description field in src/models.py
- [x] T031 [US2] Verify description is passed through to Task creation in src/task_manager.py
- [x] T032 [US2] Verify description is included in dictionary return value in src/task_manager.py

**Checkpoint (GREEN)**: Run `pytest tests/` - ALL tests (US1, US2, US3) should PASS

**Note**: Since the foundational implementation in US1 already included the description parameter as optional, US2 primarily validates that the implementation correctly handles descriptions through additional tests.

**Final Checkpoint**: At this point, all User Stories (1, 2, 3) should be independently functional. Full feature complete!

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and validation

- [x] T033 [P] Run full test suite with coverage: pytest tests/ --cov=src --cov-report=html
- [x] T034 Verify test coverage is >90% for src/models.py, src/storage.py, src/task_manager.py
- [x] T035 [P] Add edge case test for very long titles (1000+ chars) in tests/unit/test_add_task.py
- [x] T036 [P] Add edge case test for Unicode characters in title in tests/unit/test_add_task.py
- [x] T037 [P] Add edge case test for special characters (emoji) in title in tests/unit/test_add_task.py
- [x] T038 [P] Add performance test to validate <10ms task creation in tests/unit/test_add_task.py - test_add_task_performance()
- [x] T039 [P] Add timestamp accuracy test to validate SC-006 in tests/unit/test_add_task.py - test_task_timestamp_accuracy()
- [x] T040 Review and validate all acceptance criteria from spec.md are met
- [x] T041 Manual validation using quickstart.md examples
- [x] T042 Code cleanup: Remove any debug print statements, ensure consistent formatting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories 1+3 (Phase 3)**: Depends on Foundational phase completion - MVP milestone
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - Can run in parallel with Phase 3 if staffed, but logically builds on US1
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1+3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - **This is the MVP**
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Logically builds on US1 but independently testable

### Within Each User Story

**TDD Cycle (CRITICAL)**:
1. **RED**: Write tests FIRST - they MUST fail
2. **GREEN**: Implement minimum code to make tests pass
3. **REFACTOR**: Clean up code while keeping tests passing

**Task Order Within Story**:
- Tests marked [P] can run in parallel
- Implementation tasks must follow tests
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Within Phase 1 (Setup)**:
- T001 and T002 can run in parallel (different files)

**Within Phase 2 (Foundational)**:
- T003 and T004 can run in parallel (different files: models.py vs storage.py)
- T005 depends on T004 (same file)

**Within Phase 3 (US1+3 Tests)**:
- T006, T007, T008, T009, T010, T011, T012 can all run in parallel (all tests, different test functions)

**Within Phase 4 (US2 Tests)**:
- T026, T027, T028 can all run in parallel (all tests, different test functions)

**Within Phase 5 (Polish)**:
- T033, T035, T036, T037 can run in parallel (different test functions)

**Across Phases**:
- Once Foundational (Phase 2) completes, Phase 3 and Phase 4 could theoretically run in parallel with different team members
- In practice, implement Phase 3 first (MVP), validate, then Phase 4

---

## Parallel Example: User Story 1+3 Tests

```bash
# Launch all test creation tasks together (RED phase):
Task T006: "Write unit test for adding task with title only"
Task T007: "Write unit test for sequential ID generation"
Task T008: "Write unit test for task storage in memory"
Task T009: "Write unit test for empty title validation"
Task T010: "Write unit test for None title validation"
Task T011: "Write unit test for whitespace-only title validation"
Task T012: "Write integration test for complete add task flow"

# After tests written, run pytest - ALL should FAIL (RED)

# Then implement sequentially (GREEN phase):
# T013 → T014 → T015 → T016 → T017 → T018 → T019 → T020 → T021

# After implementation, run pytest - ALL should PASS (GREEN)
```

---

## Implementation Strategy

### MVP First (Recommended) 🎯

**Minimum Viable Product = User Stories 1 & 3**

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. ✅ Complete Phase 3: User Story 1 & 3 (MVP milestone!)
4. **STOP and VALIDATE**:
   - Run all tests: `pytest tests/ -v`
   - Manual test using quickstart.md examples
   - Verify all US1 and US3 acceptance criteria met
5. **Deploy/Demo MVP**: You now have a working task creation feature!
6. (Optional) Continue to Phase 4 for enhanced description functionality

### Incremental Delivery

1. **Foundation**: Setup + Foundational → Infrastructure ready
2. **MVP Release**: Add US1+US3 → Test independently → **Deploy/Demo v1.0**
3. **Enhancement Release**: Add US2 → Test independently → **Deploy/Demo v1.1**
4. Each increment adds value without breaking previous functionality

### TDD Workflow (MANDATORY)

For EVERY user story phase:

```
RED → GREEN → REFACTOR
```

1. **RED**: Write tests first, run pytest, confirm they FAIL
2. **GREEN**: Implement minimum code to pass tests, run pytest, confirm they PASS
3. **REFACTOR**: Clean up code, run pytest, confirm tests STILL PASS

**DO NOT PROCEED** to next phase until current phase passes all tests!

---

## Task Count Summary

- **Phase 1 (Setup)**: 2 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (US1+US3 - MVP)**: 20 tasks (7 tests + 9 implementation + 4 refactoring)
- **Phase 4 (US2)**: 7 tasks (3 tests + 4 verification)
- **Phase 5 (Polish)**: 10 tasks (includes performance + timestamp validation)
- **Total**: 42 tasks

### Tasks per User Story

- **User Story 1 (Add Basic Task)**: 12 tasks (5 tests + 7 implementation)
- **User Story 3 (Validation)**: 8 tasks (3 tests + 5 implementation)
- **User Story 2 (Add Description)**: 7 tasks (3 tests + 4 verification)
- **Cross-cutting (Setup, Foundational, Polish)**: 13 tasks

### Parallel Opportunities Identified

- **7 test tasks** can run in parallel within US1+US3 (Phase 3)
- **3 test tasks** can run in parallel within US2 (Phase 4)
- **2 foundational tasks** can run in parallel (Phase 2)
- **7 polish tasks** can run in parallel (Phase 5: T033, T035-T039)
- **Total parallel opportunities**: ~19 tasks (45% of all tasks)

---

## Notes

- **[P] marker**: Tasks marked [P] use different files and have no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story (US1, US2, US3) for traceability
- **TDD is mandatory**: Constitution requires test-first development (RED-GREEN-REFACTOR)
- **Each story is independently testable**: Can validate US1+US3 MVP without implementing US2
- **File paths are exact**: Every task specifies the exact file to modify
- **Checkpoint after each phase**: Validate before proceeding to next phase
- **Commit strategy**: Commit after each task or after completing a user story phase
- **MVP = Phase 1 + 2 + 3**: Delivers core value with just 25 tasks (62.5% of total)

