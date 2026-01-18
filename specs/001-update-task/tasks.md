# Tasks: Update Task Details

**Input**: Design documents from `/specs/001-update-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: This feature follows Test-Driven Development (TDD). All test tasks are written FIRST and must FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- Single project structure: `src/`, `tests/` at repository root
- Feature extends existing console application with minimal changes

---

## Phase 1: Setup & Prerequisites

**Purpose**: Verify environment and existing infrastructure

- [ ] T001 Verify on feature branch 001-update-task (not main)
- [ ] T002 Verify existing infrastructure (src/models.py, src/storage.py, tests/conftest.py) is intact
- [ ] T003 [P] Verify pytest is installed and functional
- [ ] T004 [P] Review existing add_task validation patterns in src/task_manager.py for consistency
- [ ] T005 Verify reset_task_storage fixture exists in tests/conftest.py for test isolation

**Checkpoint**: Prerequisites verified - ready for TDD workflow

---

## Phase 2: User Story 1 - Update Task Fields (Priority: P1) 🎯 MVP

**Goal**: Implement core update functionality - allow users to update task title and/or description with proper validation

**Independent Test**: Create task with add_task(), call update_task() with new field values, verify specified fields updated while immutable fields (id, completed, created_at) preserved

### RED Phase: Write Failing Tests for US1

> **CRITICAL**: These tests MUST be written FIRST and MUST FAIL before implementation

**Unit Tests - Core Update Functionality**

- [ ] T006 [P] [US1] RED: Write test for update title only in tests/unit/test_update_task.py (FR-001, FR-002, FR-006, FR-009, FR-010)
- [ ] T007 [P] [US1] RED: Write test for update description only in tests/unit/test_update_task.py (FR-001, FR-002, FR-006, FR-009, FR-010)
- [ ] T008 [P] [US1] RED: Write test for update both fields in tests/unit/test_update_task.py (FR-001, FR-002, FR-006, FR-009, FR-010)
- [ ] T009 [P] [US1] RED: Write test for immutable fields preserved (id, completed, created_at) in tests/unit/test_update_task.py (FR-007)
- [ ] T010 [P] [US1] RED: Write test for description cleared (set to None) in tests/unit/test_update_task.py (FR-008)
- [ ] T011 [P] [US1] RED: Write test for whitespace stripping in title in tests/unit/test_update_task.py (FR-015)
- [ ] T012 [P] [US1] RED: Write test for confirmation message displayed in tests/unit/test_update_task.py (FR-009)
- [ ] T013 [P] [US1] RED: Write test for return value structure (all fields) in tests/unit/test_update_task.py (FR-010)

**Run Tests - Verify RED**

- [ ] T014 [US1] RED: Run tests for US1 and verify ALL FAIL with ImportError (update_task not defined)

**Checkpoint**: US1 tests written and failing - ready for implementation

### GREEN Phase: Implement US1 to Pass Tests

- [ ] T015 [US1] GREEN: Implement update_task() function skeleton in src/task_manager.py with correct signature
- [ ] T016 [US1] GREEN: Add docstring to update_task() following project conventions
- [ ] T017 [US1] GREEN: Implement task lookup by ID in update_task() (FR-003)
- [ ] T018 [US1] GREEN: Implement title update with whitespace stripping in update_task() (FR-006, FR-015)
- [ ] T019 [US1] GREEN: Implement description update (including None to clear) in update_task() (FR-006, FR-008)
- [ ] T020 [US1] GREEN: Add confirmation message print to update_task() (FR-009)
- [ ] T021 [US1] GREEN: Implement return dictionary with all task fields in update_task() (FR-010)
- [ ] T022 [US1] GREEN: Run tests for US1 and verify ALL PASS

**Checkpoint**: US1 core functionality implemented and passing - basic update works

### Integration Tests for US1

- [ ] T023 [P] [US1] RED: Write integration test for add_task → update_task flow in tests/integration/test_update_task_flow.py
- [ ] T024 [P] [US1] RED: Write integration test for multiple tasks updated independently in tests/integration/test_update_task_flow.py
- [ ] T025 [US1] Run integration tests and verify they PASS (implementation already supports)

**Checkpoint**: US1 integration validated - works with add_task

---

## Phase 3: User Story 2 - Handle Invalid Updates (Priority: P2)

**Goal**: Implement robust error handling with clear, specific error messages for all validation failures

**Independent Test**: Call update_task() with invalid inputs (non-existent ID, empty title, no fields), verify appropriate error messages displayed and ValueError raised without state changes

### RED Phase: Write Failing Tests for US2

**Unit Tests - Error Handling**

- [ ] T026 [P] [US2] RED: Write test for task not found error in tests/unit/test_update_task.py (FR-003, FR-011, FR-014)
- [ ] T027 [P] [US2] RED: Write test for empty title error (empty string) in tests/unit/test_update_task.py (FR-005, FR-012, FR-014)
- [ ] T028 [P] [US2] RED: Write test for empty title error (whitespace only) in tests/unit/test_update_task.py (FR-005, FR-012, FR-014)
- [ ] T029 [P] [US2] RED: Write test for no fields provided error in tests/unit/test_update_task.py (FR-004, FR-013, FR-014)
- [ ] T030 [P] [US2] RED: Write test for task unchanged after error (atomicity) in tests/unit/test_update_task.py (FR-014)
- [ ] T031 [P] [US2] RED: Write test for storage empty scenario in tests/unit/test_update_task.py (FR-003, FR-011)

**Run Tests - Verify RED**

- [ ] T032 [US2] RED: Run tests for US2 and verify ALL FAIL (validation not implemented)

**Checkpoint**: US2 tests written and failing - ready for validation implementation

### GREEN Phase: Implement US2 Validation

- [ ] T033 [US2] GREEN: Implement "no fields provided" validation in update_task() (FR-004, FR-013)
- [ ] T034 [US2] GREEN: Implement "task not found" validation in update_task() (FR-003, FR-011)
- [ ] T035 [US2] GREEN: Implement "empty title" validation in update_task() (FR-005, FR-012)
- [ ] T036 [US2] GREEN: Ensure all validations raise ValueError with correct messages in update_task() (FR-014)
- [ ] T037 [US2] GREEN: Verify validation order: fields → existence → title (per research.md)
- [ ] T038 [US2] GREEN: Run tests for US2 and verify ALL PASS

**Checkpoint**: US2 error handling complete - all validation cases covered

---

## Phase 4: REFACTOR - Code Quality & Documentation

**Purpose**: Clean up implementation while maintaining all passing tests

- [ ] T039 [P] Refactor update_task() for readability (extract validation logic if needed)
- [ ] T040 [P] Add inline comments for complex validation logic in update_task()
- [ ] T041 [P] Verify docstring completeness (Args, Returns, Raises, Examples) in update_task()
- [ ] T042 Run ALL tests (US1 + US2 + integration) and verify 100% PASS after refactoring

**Checkpoint**: Code clean and documented - all tests still passing

---

## Phase 5: Edge Cases & Performance

**Purpose**: Test boundary conditions and performance requirements

### Edge Case Tests

- [ ] T043 [P] RED: Write test for long title (1000+ characters) in tests/unit/test_update_edge_cases.py
- [ ] T044 [P] RED: Write test for special characters (emojis, unicode) in tests/unit/test_update_edge_cases.py
- [ ] T045 [P] RED: Write test for rapid successive updates in tests/unit/test_update_edge_cases.py
- [ ] T046 [P] RED: Write test for both fields provided but title invalid in tests/unit/test_update_edge_cases.py
- [ ] T047 GREEN: Run edge case tests and verify they PASS (implementation should handle)

### Performance Tests

- [ ] T048 [P] Write performance test for < 10ms execution in tests/unit/test_update_edge_cases.py (SC-006)
- [ ] T049 Run performance test and verify update_task() completes in < 10ms

**Checkpoint**: Edge cases and performance validated

---

## Phase 6: Validation & Completion

**Purpose**: Verify all success criteria met and feature complete

### Success Criteria Validation

- [ ] T050 Verify SC-001: Single function call updates (run tests T006-T008)
- [ ] T051 Verify SC-002: Selective field updates preserve others (run test T009)
- [ ] T052 Verify SC-003: Description clearing works (run test T010)
- [ ] T053 Verify SC-004: Empty title rejection (run tests T027-T028)
- [ ] T054 Verify SC-005: Non-existent ID handling (run test T026)
- [ ] T055 Verify SC-006: Performance < 10ms (run test T048)

### Final Validation

- [ ] T056 Run full test suite (pytest tests/ -v) and verify ALL tests pass (unit + integration + edge cases)
- [ ] T057 Verify test count matches expectations (15+ tests for update_task)
- [ ] T058 Run coverage report (pytest --cov=src.task_manager --cov-report=term-missing) and verify 100% coverage for update_task
- [ ] T059 Verify all 15 functional requirements (FR-001 to FR-015) are tested
- [ ] T060 Verify no unresolved TODOs or placeholder comments in update_task()
- [ ] T061 Verify update_task() follows dual output pattern (print + return) per constitution
- [ ] T062 Run quickstart.md examples manually to verify they work as documented

**Checkpoint**: Feature complete - all success criteria met, tests passing, ready for commit/PR

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verify environment
- **User Story 1 (Phase 2)**: Depends on Setup - MVP functionality
- **User Story 2 (Phase 3)**: Depends on US1 - adds error handling to existing implementation
- **REFACTOR (Phase 4)**: Depends on US1 + US2 complete
- **Edge Cases (Phase 5)**: Depends on REFACTOR complete
- **Validation (Phase 6)**: Depends on all implementation phases complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - can start after Setup
- **User Story 2 (P2)**: Depends on US1 implementation (adds validation to existing function)

### Within Each User Story (TDD Workflow)

**CRITICAL ORDER**:
1. RED: Write tests FIRST - they MUST FAIL
2. GREEN: Implement MINIMAL code to pass tests
3. Tests pass before moving to next story
4. REFACTOR: Clean up while maintaining pass

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004 can run in parallel (different verification tasks)

**Phase 2 - US1 RED**:
- T006-T013 can ALL run in parallel (different test cases, same file but different functions)

**Phase 2 - US1 GREEN**:
- T015-T021 must run sequentially (same function, incremental implementation)
- T023-T024 can run in parallel (different test cases, integration tests)

**Phase 3 - US2 RED**:
- T026-T031 can ALL run in parallel (different test cases)

**Phase 3 - US2 GREEN**:
- T033-T036 must run sequentially (same function, incremental validation)

**Phase 4 - REFACTOR**:
- T039-T041 can run in parallel (different aspects: code, comments, docs)

**Phase 5 - Edge Cases**:
- T043-T046 can ALL run in parallel (different test cases)
- T048 can run in parallel with T043-T046

**Phase 6 - Validation**:
- T050-T055 can run in parallel (independent verifications)
- T056-T062 should run sequentially (depends on test suite completion)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Launch all US1 unit tests together (T006-T013):
Task: "Write test for update title only in tests/unit/test_update_task.py"
Task: "Write test for update description only in tests/unit/test_update_task.py"
Task: "Write test for update both fields in tests/unit/test_update_task.py"
Task: "Write test for immutable fields preserved in tests/unit/test_update_task.py"
Task: "Write test for description cleared in tests/unit/test_update_task.py"
Task: "Write test for whitespace stripping in tests/unit/test_update_task.py"
Task: "Write test for confirmation message in tests/unit/test_update_task.py"
Task: "Write test for return value structure in tests/unit/test_update_task.py"

# Then T014: Run all tests to verify they FAIL
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: User Story 1 (T006-T025)
   - RED: Write tests (T006-T014)
   - GREEN: Implement (T015-T022)
   - Integration: Test with add_task (T023-T025)
3. **STOP and VALIDATE**: User Story 1 is now a working MVP
   - Can update task title
   - Can update task description
   - Can update both fields
   - Immutable fields preserved
   - Integration with add_task works

### Incremental Delivery

1. MVP: User Story 1 → Basic update works
2. Robust: User Story 2 → Error handling complete
3. Production-Ready: Edge cases + Performance → All scenarios covered
4. Polished: REFACTOR + Validation → Clean, documented, verified

### TDD Workflow (CRITICAL)

**RED → GREEN → REFACTOR cycle for EACH user story**:

1. **RED Phase**:
   - Write ALL tests for the user story
   - Run tests - they MUST FAIL (ImportError or assertion failures)
   - Do NOT proceed to GREEN until tests fail correctly

2. **GREEN Phase**:
   - Write MINIMAL code to make tests pass
   - Run tests frequently
   - Once all tests pass, STOP coding

3. **REFACTOR Phase**:
   - Clean up code
   - Improve readability
   - Add documentation
   - Run tests after each change - they MUST stay green

4. **Next Story**:
   - Return to RED phase for next user story
   - Repeat cycle

---

## Notes

- **[P] tasks**: Different files or independent work - can run in parallel
- **[Story] label**: Maps task to specific user story (US1, US2) for traceability
- **TDD is MANDATORY**: Tests written FIRST, implementation SECOND
- **Each user story is independently testable**: US1 can be validated without US2
- **Fail-fast validation**: RED tests MUST fail before writing implementation
- **Minimal implementation**: Only write code to pass tests (GREEN phase)
- **Test coverage**: Target 100% coverage for update_task() function
- **Performance**: Every update must complete in < 10ms (SC-006)
- **Atomicity**: Validation failures leave task unchanged (no partial updates)
- **Consistency**: Follow add_task patterns (dual output, validation, error messages)

### Critical Success Factors

1. ✅ Tests written BEFORE implementation
2. ✅ Tests FAIL initially (RED phase)
3. ✅ Minimal implementation to pass tests (GREEN phase)
4. ✅ Clean code with tests still passing (REFACTOR phase)
5. ✅ Each user story independently testable
6. ✅ 100% test coverage for update_task()
7. ✅ All 15 functional requirements tested
8. ✅ Performance < 10ms verified
9. ✅ All 6 success criteria validated
10. ✅ Integration with existing features (add_task) confirmed

---

## Task Summary

**Total Tasks**: 62
**Phases**: 6

### Task Breakdown by Phase

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (US1 - MVP)**: 20 tasks
  - RED: 9 tests
  - GREEN: 8 implementation + 1 verification
  - Integration: 3 tests
- **Phase 3 (US2 - Error Handling)**: 13 tasks
  - RED: 7 tests
  - GREEN: 6 implementation
- **Phase 4 (REFACTOR)**: 4 tasks
- **Phase 5 (Edge Cases)**: 7 tasks
- **Phase 6 (Validation)**: 13 tasks

### Parallel Opportunities

- **Setup**: 2 parallel tasks (T003, T004)
- **US1 RED**: 8 parallel tests (T006-T013)
- **US1 Integration**: 2 parallel tests (T023-T024)
- **US2 RED**: 6 parallel tests (T026-T031)
- **REFACTOR**: 3 parallel tasks (T039-T041)
- **Edge Cases**: 5 parallel tests (T043-T048)
- **Validation SC**: 6 parallel verifications (T050-T055)

**Total Parallel Opportunities**: ~32 tasks can run in parallel with proper coordination

### Independent Test Criteria

**User Story 1 (MVP)**:
- ✅ Create task with add_task()
- ✅ Call update_task(id, title="New")
- ✅ Verify title changed, description/id/completed/created_at unchanged
- ✅ Confirmation message displayed
- ✅ Result: Working update functionality

**User Story 2 (Error Handling)**:
- ✅ Call update_task(999, title="New") → ValueError "Task #999 not found"
- ✅ Call update_task(1, title="") → ValueError "Task title cannot be empty"
- ✅ Call update_task(1) → ValueError "No fields to update"
- ✅ Verify task unchanged after error
- ✅ Result: Robust error handling

### Suggested MVP Scope

**Minimum Viable Product**: User Story 1 ONLY (Phase 1 + Phase 2)
- **Tasks**: T001-T025 (25 tasks)
- **Deliverable**: Basic update functionality that works with add_task
- **Value**: Users can update task title and/or description
- **Testable**: Complete, independently verifiable feature
- **Next Increment**: Add User Story 2 for production-ready error handling
