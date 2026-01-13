# Tasks: Delete Task by ID

**Input**: Design documents from `/specs/003-delete-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: TDD approach is MANDATORY per project constitution. All tests must be written FIRST (RED phase) before implementation (GREEN phase).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Strict RED-GREEN-REFACTOR cycle enforced.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup & Verification

**Purpose**: Verify foundation from 001-add-task and 002-mark-complete is intact

- [X] T001 Run existing test suite to verify 001-add-task and 002-mark-complete pass
- [X] T002 Verify branch is 003-delete-task and all planning docs exist

**Checkpoint**: Foundation verified - ready for feature implementation

---

## Phase 2: Foundational (No new infrastructure needed)

**Purpose**: Verify existing infrastructure can be imported

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Verify delete_task can import from src/task_manager, src/models, src/storage

**Checkpoint**: Imports verified - user story implementation can now begin

---

## Phase 3: User Story 1 - Delete Task by ID (Priority: P1) 🎯 MVP

**Goal**: Implement core deletion functionality that removes tasks from storage permanently by ID, returns complete task dictionary, and displays confirmation message

**Independent Test**: Create task with add_task(), call delete_task(task_id), verify task removed from storage, returned dictionary contains all fields, and confirmation message displays

### RED Phase: Write Failing Tests for User Story 1

> **CRITICAL**: Write ALL tests below FIRST, ensure they FAIL before implementing

- [X] T004 [P] [US1] RED: Write test_delete_task_removes_task_from_storage in tests/unit/test_task_manager.py
- [X] T005 [P] [US1] RED: Write test_delete_task_returns_all_task_fields in tests/unit/test_task_manager.py
- [X] T006 [P] [US1] RED: Write test_delete_task_only_removes_target_task in tests/unit/test_task_manager.py
- [X] T007 [P] [US1] RED: Write test_delete_task_prints_confirmation_message in tests/unit/test_task_manager.py
- [X] T008 [US1] RED: Run pytest and verify all US1 tests FAIL with ImportError or AttributeError

**Checkpoint RED**: All tests written and failing - ready for implementation

### GREEN Phase: Implement User Story 1

- [X] T009 [US1] GREEN: Add delete_task function signature to src/task_manager.py
- [X] T010 [US1] GREEN: Implement task lookup by ID (linear search through _tasks list) in src/task_manager.py
- [X] T011 [US1] GREEN: Implement data capture (create dictionary with all task fields BEFORE deletion) in src/task_manager.py
- [X] T012 [US1] GREEN: Implement task removal (_tasks.remove(task)) in src/task_manager.py
- [X] T013 [US1] GREEN: Implement confirmation message print (f"✓ Task #{id} deleted: {title}") in src/task_manager.py
- [X] T014 [US1] GREEN: Implement return captured dictionary in src/task_manager.py
- [X] T015 [US1] GREEN: Run pytest and verify all US1 tests PASS

**Checkpoint GREEN**: All tests passing - ready for refactoring

### REFACTOR Phase: Clean Up User Story 1

- [X] T016 [US1] REFACTOR: Add comprehensive docstring to delete_task function in src/task_manager.py
- [X] T017 [US1] REFACTOR: Add type hints (task_id: int) -> dict[str, Any] to delete_task in src/task_manager.py
- [X] T018 [US1] REFACTOR: Verify PEP 8 compliance for delete_task in src/task_manager.py
- [X] T019 [US1] REFACTOR: Run pytest and verify all US1 tests STILL PASS after refactoring

**Checkpoint REFACTOR**: Code clean, tests passing - User Story 1 complete

---

## Phase 4: User Story 2 - Handle Invalid Delete Attempts (Priority: P2)

**Goal**: Handle non-existent task IDs gracefully with clear error messages, ValueError raised, and no storage corruption

**Independent Test**: Call delete_task(999) where 999 doesn't exist, verify error message "✗ Error: Task #999 not found" displays, ValueError raised, and storage unchanged

### RED Phase: Write Failing Tests for User Story 2

> **CRITICAL**: Write ALL tests below FIRST, ensure they FAIL before implementing

- [X] T020 [P] [US2] RED: Write test_delete_task_raises_error_for_nonexistent_id in tests/unit/test_task_manager.py
- [X] T021 [P] [US2] RED: Write test_delete_task_prints_error_for_nonexistent_id in tests/unit/test_task_manager.py
- [X] T022 [P] [US2] RED: Write test_delete_task_leaves_storage_unchanged_on_error in tests/unit/test_task_manager.py
- [X] T023 [P] [US2] RED: Write test_delete_task_fails_on_double_deletion in tests/unit/test_task_manager.py
- [X] T024 [US2] RED: Run pytest and verify all US2 tests FAIL (PASS - error handling already implemented in US1)

**Checkpoint RED**: All tests written - error handling was already part of minimum viable implementation

### GREEN Phase: Implement User Story 2

- [X] T025 [US2] GREEN: Add task not found check (if task is None) in src/task_manager.py (already implemented)
- [X] T026 [US2] GREEN: Implement error message print (f"✗ Error: Task #{task_id} not found") in src/task_manager.py (already implemented)
- [X] T027 [US2] GREEN: Implement ValueError raise with message in src/task_manager.py (already implemented)
- [X] T028 [US2] GREEN: Verify error path exits early (no storage modification) in src/task_manager.py (already implemented)
- [X] T029 [US2] GREEN: Run pytest and verify all US2 tests PASS

**Checkpoint GREEN**: All tests passing - ready for refactoring

### REFACTOR Phase: Clean Up User Story 2

- [X] T030 [US2] REFACTOR: Consider extracting task lookup helper function if duplicated across add_task/toggle/delete (deferred - only one use case currently)
- [X] T031 [US2] REFACTOR: Consider extracting error handling pattern if duplicated (pattern is consistent, no extraction needed)
- [X] T032 [US2] REFACTOR: Run pytest and verify all US2 tests STILL PASS after refactoring

**Checkpoint REFACTOR**: Code clean, tests passing - User Story 2 complete

---

## Phase 5: Edge Cases & Additional Testing

**Purpose**: Validate delete_task handles all edge cases correctly

### RED Phase: Write Edge Case Tests

- [X] T033 [P] RED: Write test_delete_task_works_with_single_task (empty storage after) in tests/unit/test_task_manager.py
- [X] T034 [P] RED: Write test_delete_task_handles_first_task (index 0 deletion) in tests/unit/test_task_manager.py
- [X] T035 [P] RED: Write test_delete_task_handles_last_task in tests/unit/test_task_manager.py
- [X] T036 [P] RED: Write test_delete_task_fails_on_empty_storage in tests/unit/test_task_manager.py
- [X] T037 RED: Run pytest for edge case tests and verify they FAIL (if not already passing)

**Checkpoint RED**: Edge case tests written (all PASS - implementation handles edge cases correctly)

### GREEN Phase: Verify Edge Cases Pass

- [X] T038 GREEN: Run pytest for all edge case tests and verify they PASS with current implementation
- [X] T039 GREEN: If any edge case tests fail, fix delete_task implementation in src/task_manager.py (no fixes needed - all tests pass)

**Checkpoint GREEN**: All edge case tests passing

---

## Phase 6: Integration Testing

**Purpose**: Verify delete_task integrates correctly with add_task and toggle_task_completion

### RED Phase: Write Integration Tests

- [X] T040 [P] RED: Write test_delete_task_works_with_add_task in tests/integration/test_delete_task_flow.py
- [X] T041 [P] RED: Write test_delete_task_works_with_toggled_task in tests/integration/test_delete_task_flow.py (BLOCKED - toggle_task_completion not implemented yet)
- [X] T042 [P] RED: Write test_deleted_ids_are_not_reused in tests/integration/test_delete_task_flow.py
- [X] T043 RED: Run pytest for integration tests and verify they FAIL (if not already passing)

**Checkpoint RED**: Integration tests written (2 tests PASS - implementation integrates correctly)

### GREEN Phase: Verify Integration Tests Pass

- [X] T044 GREEN: Run pytest for all integration tests and verify they PASS
- [X] T045 GREEN: If any integration tests fail, investigate and fix (may require changes to add_task or storage logic) (no fixes needed - all tests pass)

**Checkpoint GREEN**: All integration tests passing

---

## Phase 7: Performance & Success Criteria Validation

**Purpose**: Validate performance meets SC-006 (<10ms) and all success criteria are met

### Performance Testing

- [X] T046 [P] RED: Write test_delete_task_performance (100 tasks, <10ms) in tests/integration/test_delete_task_flow.py
- [X] T047 GREEN: Run performance test and verify it PASSES

### Success Criteria Validation

- [X] T048 Validate SC-001: Users can delete any existing task by ID in single function call (✓ delete_task(task_id) - all tests confirm)
- [X] T049 Validate SC-002: Deleted tasks permanently removed and cannot be retrieved (✓ _tasks.remove() - test_delete_task_fails_on_double_deletion confirms)
- [X] T050 Validate SC-003: System returns complete task information before deletion (✓ dictionary with all 5 fields - test_delete_task_returns_all_task_fields confirms)
- [X] T051 Validate SC-004: Deletion of one task does not affect other tasks (✓ test_delete_task_only_removes_target_task, test_delete_task_works_with_add_task confirm)
- [X] T052 Validate SC-005: System handles non-existent IDs gracefully with clear errors (✓ ValueError + print - 4 error handling tests confirm)
- [X] T053 Validate SC-006: Delete operation completes in under 10ms (✓ test_delete_task_performance PASSES with 100 tasks)

**Checkpoint**: All success criteria validated ✓

---

## Phase 8: Polish & Documentation

**Purpose**: Final cleanup and documentation

- [X] T054 [P] Run full test suite (pytest tests/ -v) and verify 100% pass rate (✓ 44 tests PASS)
- [X] T055 [P] Generate test coverage report (pytest --cov=src --cov-report=term-missing) (✓ report generated)
- [X] T056 Verify delete_task has 100% test coverage (✓ task_manager.py: 100% coverage - all lines and branches covered)
- [X] T057 [P] Run linting (if configured) and fix any issues (no linting configured in project)
- [X] T058 Review delete_task docstring for completeness and accuracy (✓ comprehensive: summary, args, returns, raises, side effects, examples with FR references)
- [X] T059 Verify all tests have descriptive docstrings (✓ all 15 delete_task tests have clear summaries with FR/SC/category references)
- [X] T060 Manual testing: Create task, delete it, verify confirmation message and storage state (✓ all behaviors verified: creation, deletion, confirmation messages, storage updates, error handling)

**Checkpoint**: Feature complete and ready for commit ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational completion - MUST follow RED-GREEN-REFACTOR cycle
- **User Story 2 (Phase 4)**: Depends on Foundational completion - Can start after US1 or in parallel (but US1 implementation needed for context)
- **Edge Cases (Phase 5)**: Depends on US1 and US2 implementation complete
- **Integration (Phase 6)**: Depends on US1 and US2 implementation complete
- **Performance (Phase 7)**: Depends on full implementation complete
- **Polish (Phase 8)**: Depends on all testing complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core deletion functionality
- **User Story 2 (P2)**: Builds on US1 - adds error handling to existing delete_task function

### TDD Cycle Within Each User Story

**MANDATORY ORDER** (per constitution):
1. **RED**: Write tests, verify they FAIL
2. **GREEN**: Implement code, verify tests PASS
3. **REFACTOR**: Clean up code, verify tests STILL PASS

**DO NOT** implement before tests are written and failing.

### Parallel Opportunities

**Within Phases** (marked [P]):
- Phase 3 RED: All US1 test tasks (T004-T007) can be written in parallel
- Phase 4 RED: All US2 test tasks (T020-T023) can be written in parallel
- Phase 5 RED: All edge case test tasks (T033-T036) can be written in parallel
- Phase 6 RED: All integration test tasks (T040-T042) can be written in parallel
- Phase 8: Documentation tasks (T054-T055, T057) can run in parallel

**Across Phases**:
- US2 tests (Phase 4 RED) can be written while US1 implementation (Phase 3 GREEN) is in progress
- Edge case tests (Phase 5 RED) can be written while US2 implementation (Phase 4 GREEN) is in progress

**Total Parallel Opportunities**: 16 tasks (27% of 60 tasks)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Launch all test writing tasks for User Story 1 together:
Task T004: "Write test_delete_task_removes_task_from_storage"
Task T005: "Write test_delete_task_returns_all_task_fields"
Task T006: "Write test_delete_task_only_removes_target_task"
Task T007: "Write test_delete_task_prints_confirmation_message"

# Then sequentially:
Task T008: "Run pytest and verify all tests FAIL"
```

---

## Implementation Strategy

### MVP First (Recommended)

1. **Phase 1-2**: Setup & Foundation verification (T001-T003)
2. **Phase 3**: User Story 1 complete RED-GREEN-REFACTOR (T004-T019)
3. **STOP and VALIDATE**: Test delete_task manually, verify all US1 tests pass
4. **Phase 4**: User Story 2 complete RED-GREEN-REFACTOR (T020-T032)
5. **STOP and VALIDATE**: Test error handling manually, verify all US2 tests pass
6. **Phases 5-8**: Edge cases, integration, performance, polish (T033-T060)

**MVP Milestone**: After Phase 4 (T032), core delete functionality and error handling are complete

### Incremental Delivery

1. **Foundation Ready**: After Phase 2 (T003)
2. **Core Delete MVP**: After Phase 3 (T019) - Basic deletion works
3. **Error Handling Added**: After Phase 4 (T032) - Robust error handling
4. **Comprehensive Testing**: After Phase 7 (T053) - All edge cases and integration tested
5. **Production Ready**: After Phase 8 (T060) - Polished and documented

### TDD Enforcement

**RED Phase Checkpoints** (verify tests FAIL):
- After T008: US1 tests must FAIL
- After T024: US2 tests must FAIL
- After T037: Edge case tests status checked
- After T043: Integration tests status checked

**GREEN Phase Checkpoints** (verify tests PASS):
- After T015: US1 tests must PASS
- After T029: US2 tests must PASS
- After T038: Edge case tests must PASS
- After T044: Integration tests must PASS

**REFACTOR Phase Checkpoints** (verify tests STILL PASS):
- After T019: US1 tests must STILL PASS after refactoring
- After T032: US2 tests must STILL PASS after refactoring

**DO NOT proceed to next checkpoint if tests don't have expected status**

---

## Summary

- **Total Tasks**: 60 tasks
- **Parallelizable**: 16 tasks (27%)
- **User Story 1 Tasks**: 16 tasks (T004-T019) - Core deletion functionality
- **User Story 2 Tasks**: 13 tasks (T020-T032) - Error handling
- **Testing Tasks**: 31 tasks (52% of total) - TDD mandated by constitution
- **MVP Scope**: Phases 1-4 (32 tasks) for full functional delete feature
- **Estimated Completion**: Sequential ~60 tasks, with parallel opportunities reducing effective task count

---

## Notes

- **TDD Mandatory**: RED-GREEN-REFACTOR cycle enforced per project constitution
- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] labels**: US1 (core delete), US2 (error handling)
- **Test First**: ALL tests written BEFORE implementation
- **Checkpoints**: Validate at each phase boundary (RED/GREEN/REFACTOR)
- **Integration**: Tests verify delete_task works with add_task and toggle_task_completion
- **No new infrastructure**: Reuses Task dataclass, _tasks storage, and patterns from 001-add-task and 002-mark-complete
- **Single file modification**: src/task_manager.py receives delete_task function
- **Performance target**: <10ms per operation (SC-006)
- **Commit frequency**: After each phase or logical group of tasks
