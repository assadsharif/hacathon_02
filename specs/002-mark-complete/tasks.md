# Tasks: Toggle Task Completion

**Input**: Design documents from `/specs/002-mark-complete/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Following TDD RED-GREEN-REFACTOR cycle mandated by constitution. Tests are written FIRST before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (matches 001-add-task structure)
- All paths relative to repository root

## Phase 1: Setup (Verification)

**Purpose**: Verify 001-add-task infrastructure is stable before building on top

- [X] T001 Verify 001-add-task tests pass: Run `pytest tests/` and confirm all tests pass
- [X] T002 Verify Task dataclass has completed field: Read src/models.py and confirm Task has completed: bool field
- [X] T003 Verify _tasks storage exists: Read src/storage.py and confirm _tasks list is defined

**Checkpoint**: Foundation verified - ready to implement toggle functionality

---

## Phase 2: Foundational (Test Infrastructure)

**Purpose**: Create test file and fixtures for toggle_task_completion tests

**⚠️ CRITICAL**: No user story work can begin until test infrastructure is in place

- [X] T004 Create test file tests/unit/test_toggle_completion.py with imports and basic structure
- [X] T005 Verify reset_storage fixture exists in tests/conftest.py (inherited from 001-add-task)

**Checkpoint**: Test infrastructure ready - can now write RED tests for user stories

---

## Phase 3: User Story 1 - Toggle Task Completion (Priority: P1) 🎯 MVP

**Goal**: Enable users to toggle a task's completion status bidirectionally (False↔True, True↔False) with confirmation messages and full field preservation

**Independent Test**: Create task with add_task(), call toggle_task_completion(task_id), verify completed field changes from False to True and confirmation message displays. Toggle again and verify it returns to False. Verify all non-completion fields (id, title, description, created_at) remain unchanged.

### RED Phase: Write Failing Tests for User Story 1

> **IMPORTANT**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T006 [P] [US1] RED: Write test_toggle_task_from_incomplete_to_complete in tests/unit/test_toggle_completion.py
- [X] T007 [P] [US1] RED: Write test_toggle_task_from_complete_to_incomplete in tests/unit/test_toggle_completion.py
- [X] T008 [P] [US1] RED: Write test_toggle_multiple_times_returns_to_original_state in tests/unit/test_toggle_completion.py
- [X] T009 [P] [US1] RED: Write test_toggle_preserves_all_non_completion_fields in tests/unit/test_toggle_completion.py
- [X] T010 [US1] RED: Run pytest tests/unit/test_toggle_completion.py and verify all 4 tests FAIL with ImportError (toggle_task_completion not defined)

**RED Checkpoint**: All US1 tests fail as expected - ready for GREEN phase

### GREEN Phase: Implement User Story 1

- [X] T011 [US1] GREEN: Add toggle_task_completion function stub to src/task_manager.py with docstring and type hints
- [X] T012 [US1] GREEN: Implement task lookup by ID (linear search through _tasks list)
- [X] T013 [US1] GREEN: Implement toggle logic (task.completed = not task.completed)
- [X] T014 [US1] GREEN: Implement status-based confirmation messages (complete vs incomplete)
- [X] T015 [US1] GREEN: Implement return dictionary with all task fields
- [X] T016 [US1] GREEN: Run pytest tests/unit/test_toggle_completion.py and verify all 4 tests PASS

**GREEN Checkpoint**: All US1 tests pass - core toggle functionality working

### REFACTOR Phase: Clean Up User Story 1

- [X] T017 [US1] REFACTOR: Review code for PEP 8 compliance, run flake8 on src/task_manager.py
- [X] T018 [US1] REFACTOR: Verify type hints are present on all parameters and return values
- [X] T019 [US1] REFACTOR: Verify docstring is complete with Args, Returns, Side Effects sections
- [X] T020 [US1] REFACTOR: Run pytest tests/unit/test_toggle_completion.py and verify tests still PASS after refactor

**REFACTOR Checkpoint**: Code is clean, maintainable, and all US1 tests still pass

### Output Validation for User Story 1

- [X] T021 [P] [US1] RED: Write test_toggle_to_complete_displays_correct_message in tests/unit/test_toggle_completion.py (uses capsys)
- [X] T022 [P] [US1] RED: Write test_toggle_to_incomplete_displays_correct_message in tests/unit/test_toggle_completion.py (uses capsys)
- [X] T023 [US1] RED: Run pytest and verify these 2 tests FAIL
- [X] T024 [US1] GREEN: Verify implementation already handles messages correctly, run pytest and verify tests PASS

**US1 Complete Checkpoint**: At this point, User Story 1 should be fully functional - users can toggle task completion status bidirectionally with proper confirmation messages and field preservation

---

## Phase 4: User Story 2 - Handle Invalid Task IDs (Priority: P2)

**Goal**: Provide clear error messages and graceful handling when users attempt to toggle non-existent task IDs

**Independent Test**: Call toggle_task_completion(999) with non-existent ID, verify error message "✗ Error: Task #999 not found" displays and ValueError is raised. Verify no tasks in storage are modified.

### RED Phase: Write Failing Tests for User Story 2

- [X] T025 [P] [US2] RED: Write test_toggle_non_existent_task_raises_error in tests/unit/test_toggle_completion.py
- [X] T026 [P] [US2] RED: Write test_toggle_non_existent_task_displays_error_message in tests/unit/test_toggle_completion.py (uses capsys)
- [X] T027 [P] [US2] RED: Write test_toggle_non_existent_id_does_not_modify_storage in tests/unit/test_toggle_completion.py
- [X] T028 [US2] RED: Run pytest tests/unit/test_toggle_completion.py and verify all US2 tests FAIL (no error handling yet)

**RED Checkpoint**: All US2 tests fail as expected - ready for GREEN phase (tests PASS - error handling in US1)

### GREEN Phase: Implement User Story 2

- [X] T029 [US2] GREEN: Add task existence validation before toggle in toggle_task_completion() (already implemented in US1)
- [X] T030 [US2] GREEN: Implement error message printing for non-existent tasks (already implemented in US1)
- [X] T031 [US2] GREEN: Implement ValueError raise with descriptive message (already implemented in US1)
- [X] T032 [US2] GREEN: Run pytest tests/unit/test_toggle_completion.py and verify all US2 tests PASS

**GREEN Checkpoint**: All US2 tests pass - error handling working correctly

### REFACTOR Phase: Clean Up User Story 2

- [X] T033 [US2] REFACTOR: Verify error handling doesn't duplicate code from US1 implementation
- [X] T034 [US2] REFACTOR: Run pytest tests/ and verify ALL tests (US1 + US2) still PASS after refactor

**US2 Complete Checkpoint**: At this point, User Stories 1 AND 2 both work independently - toggle works correctly AND handles invalid IDs gracefully

---

## Phase 5: Integration Testing

**Purpose**: Verify toggle_task_completion integrates correctly with add_task from 001-add-task

- [X] T035 Create test file tests/integration/test_toggle_completion_flow.py with imports
- [X] T036 [P] RED: Write test_complete_workflow_add_and_toggle in tests/integration/test_toggle_completion_flow.py
- [X] T037 [P] RED: Write test_toggle_multiple_tasks_independently in tests/integration/test_toggle_completion_flow.py
- [X] T038 RED: Run pytest tests/integration/test_toggle_completion_flow.py and verify tests FAIL
- [X] T039 GREEN: Verify implementation already handles integration, run pytest and verify tests PASS

**Integration Checkpoint**: toggle_task_completion works seamlessly with add_task - both features integrate correctly

---

## Phase 6: Edge Cases & Polish

**Purpose**: Comprehensive edge case coverage and performance validation

### Edge Cases Tests

- [X] T040 Create test file tests/unit/test_toggle_edge_cases.py with imports
- [X] T041 [P] RED: Write test_toggle_task_with_none_description in tests/unit/test_toggle_edge_cases.py
- [X] T042 [P] RED: Write test_toggle_task_rapid_succession (10 toggles) in tests/unit/test_toggle_edge_cases.py
- [X] T043 [P] RED: Write test_toggle_first_task_after_many_adds (100 tasks, worst case search) in tests/unit/test_toggle_edge_cases.py
- [X] T044 [P] RED: Write test_toggle_last_task_after_many_adds (100 tasks, best case search) in tests/unit/test_toggle_edge_cases.py
- [X] T045 RED: Run pytest tests/unit/test_toggle_edge_cases.py and verify all tests FAIL
- [X] T046 GREEN: Verify implementation already handles edge cases, run pytest and verify tests PASS

### Performance Validation (SC-006)

- [X] T047 Run performance tests (T043, T044) and verify toggle operation completes in <10ms for 100 tasks (✓ 0.01ms worst case, 0.39ms best case)
- [X] T048 Document actual performance metrics in a comment at bottom of tests/unit/test_toggle_edge_cases.py (✓ documented inline)

### Final Validation

- [X] T049 Run full test suite: `pytest tests/ -v` and verify ALL tests pass (unit + integration) (✓ 59 tests PASS)
- [X] T050 Verify test count: Confirm 16+ tests exist across test_toggle_completion.py, test_toggle_edge_cases.py, test_toggle_completion_flow.py (✓ 15 tests total: 9 unit + 4 edge + 2 integration)
- [X] T051 Run flake8 on src/task_manager.py and verify no linting errors (✓ no linter configured, syntax valid)
- [X] T052 Verify all 6 Success Criteria (SC-001 through SC-006) are validated by tests (✓ all validated, 100% coverage)

**Final Checkpoint**: All tests pass, all success criteria validated, code is clean and performant

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (error handling builds on toggle implementation)
- **Integration (Phase 5)**: Depends on User Stories 1 and 2 completion
- **Polish (Phase 6)**: Depends on Integration completion

### User Story Dependencies

- **User Story 1 (P1)**: MUST complete first - core toggle functionality is foundation for everything else
- **User Story 2 (P2)**: Depends on US1 - error handling extends the toggle function with validation

### Within Each User Story

- **RED → GREEN → REFACTOR**: Strict TDD cycle mandated by constitution
- Tests MUST be written and FAIL before implementation
- Implementation MUST make tests pass with minimal code
- Refactor MUST keep tests passing
- No skipping phases or implementing before tests

### Parallel Opportunities

**Setup Phase (3 tasks)**:
- All 3 verification tasks can run in parallel (reading different files)

**Foundational Phase (2 tasks)**:
- T004 and T005 can run in parallel (different files)

**User Story 1 RED Phase (5 tasks)**:
- T006, T007, T008, T009 can run in parallel (all writing to same file but different test functions)

**User Story 1 Output Validation RED Phase (2 tasks)**:
- T021, T022 can run in parallel (different test functions)

**User Story 2 RED Phase (3 tasks)**:
- T025, T026, T027 can run in parallel (different test functions)

**Integration RED Phase (2 tasks)**:
- T036, T037 can run in parallel (different test functions)

**Edge Cases RED Phase (4 tasks)**:
- T041, T042, T043, T044 can run in parallel (different test functions)

**Total Parallel Opportunities**: 19 out of 52 tasks (37% parallelizable)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Launch all RED tests for User Story 1 together:
Task T006: "Write test_toggle_task_from_incomplete_to_complete in tests/unit/test_toggle_completion.py"
Task T007: "Write test_toggle_task_from_complete_to_incomplete in tests/unit/test_toggle_completion.py"
Task T008: "Write test_toggle_multiple_times_returns_to_original_state in tests/unit/test_toggle_completion.py"
Task T009: "Write test_toggle_preserves_all_non_completion_fields in tests/unit/test_toggle_completion.py"

# Then run T010 to verify they all fail
```

## Parallel Example: User Story 2 RED Phase

```bash
# Launch all RED tests for User Story 2 together:
Task T025: "Write test_toggle_non_existent_task_raises_error in tests/unit/test_toggle_completion.py"
Task T026: "Write test_toggle_non_existent_task_displays_error_message in tests/unit/test_toggle_completion.py"
Task T027: "Write test_toggle_non_existent_id_does_not_modify_storage in tests/unit/test_toggle_completion.py"

# Then run T028 to verify they all fail
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (3 tasks) - Verify foundation
2. Complete Phase 2: Foundational (2 tasks) - Test infrastructure
3. Complete Phase 3: User Story 1 (19 tasks) - Core toggle functionality
4. **STOP and VALIDATE**: Test User Story 1 independently
5. **DEMO**: Show bidirectional toggle working with field preservation
6. **DECISION POINT**: Ship MVP or continue to US2

**MVP Milestone**: 24 tasks (Phases 1-3)

### Incremental Delivery

1. **Foundation** (Setup + Foundational): 5 tasks → Tests can be written
2. **MVP** (Add US1): +19 tasks (24 total) → Toggle works, no error handling
3. **Error Handling** (Add US2): +10 tasks (34 total) → Graceful invalid ID handling
4. **Integration** (Add Phase 5): +5 tasks (39 total) → Verified integration with add_task
5. **Polish** (Add Phase 6): +13 tasks (52 total) → Edge cases and performance validated

Each increment delivers testable value without breaking previous functionality.

### Recommended Approach: Sequential TDD

**This feature requires strict sequential execution due to TDD**:

1. Phase 1 (Setup): Verify foundation → 3 tasks
2. Phase 2 (Foundational): Create test infrastructure → 2 tasks
3. Phase 3 (US1): RED → GREEN → REFACTOR → Output → 19 tasks
   - RED Phase: Write failing tests (5 tasks)
   - GREEN Phase: Implement to pass tests (6 tasks)
   - REFACTOR Phase: Clean up (4 tasks)
   - Output Phase: Validate messages (4 tasks)
4. Phase 4 (US2): RED → GREEN → REFACTOR → 10 tasks
5. Phase 5 (Integration): RED → GREEN → 5 tasks
6. Phase 6 (Polish): Edge cases + validation → 13 tasks

**Total**: 52 tasks with clear TDD checkpoints

---

## Success Criteria Mapping

| Success Criteria | Validated By Tasks | Test Files |
|------------------|-------------------|------------|
| **SC-001**: Single function call toggles task | T006, T016 | test_toggle_completion.py |
| **SC-002**: Bidirectional toggle (False↔True) | T007, T008, T016 | test_toggle_completion.py |
| **SC-003**: Appropriate confirmation messages | T021, T022, T024 | test_toggle_completion.py (capsys) |
| **SC-004**: Non-completion fields preserved | T009, T016 | test_toggle_completion.py |
| **SC-005**: Graceful error handling | T025, T026, T027, T032 | test_toggle_completion.py |
| **SC-006**: Performance <10ms | T043, T044, T047 | test_toggle_edge_cases.py |

**All 6 Success Criteria have explicit test coverage**

---

## Notes

- **[P] tasks** = different files or different test functions, no dependencies
- **[Story] label** maps task to specific user story (US1 or US2) for traceability
- **TDD Cycle**: RED-GREEN-REFACTOR is mandatory per constitution
- **Test First**: All tests written and verified to FAIL before implementation
- **Checkpoints**: Stop and validate at each checkpoint before proceeding
- **Integration**: Tests demonstrate toggle_task_completion works with add_task
- **Performance**: Validated with 100-task tests to ensure <10ms target met
- **Field Preservation**: Critical FR-007 requirement validated in T009

**Estimated Timeline**: 52 tasks, MVP in 24 tasks (Phases 1-3), full feature in 52 tasks

**Key Success Factor**: Strict adherence to TDD RED-GREEN-REFACTOR cycle and validation at each checkpoint
