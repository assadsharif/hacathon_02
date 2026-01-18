# Feature Specification: Toggle Task Completion Status

**Feature Branch**: `002-mark-complete`
**Created**: 2026-01-13
**Status**: Draft
**Input**: User description: "Convert mark-complete feature from Phase I spec. User story: As a user, I want to toggle a task's completion status (mark complete/incomplete) so I can track my progress. Key requirements: (1) Accept task ID as input, (2) Toggle completed field between True/False, (3) Return updated task dictionary, (4) Display confirmation with new status, (5) Handle non-existent task IDs with clear error. Technical: Function signature toggle_task_completion(task_id: int) -> dict[str, Any]. Toggle behavior: False→True or True→False. Confirmation messages: '✓ Task #{id} marked as complete' or '✓ Task #{id} marked as incomplete'. Error: '✗ Error: Task #{id} not found' when ID doesn't exist. All other task fields (title, description, created_at) remain unchanged. Builds on 001-add-task foundation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Toggle Task Completion (Priority: P1)

As a user, I want to toggle a task's completion status so I can mark tasks as complete when finished and mark them as incomplete if I need to work on them again.

**Why this priority**: This is the core functionality that enables users to track their progress. Without the ability to mark tasks as complete, users cannot distinguish between finished and unfinished work. This is essential for any task management system and represents the minimum viable product for this feature.

**Independent Test**: Can be fully tested by creating a task with add_task(), calling toggle_task_completion() with the task ID, and verifying the completed field changes from False to True (or vice versa) and the appropriate confirmation message is displayed. Delivers immediate value by allowing users to track completed work.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1 and completed=False, **When** user calls toggle_task_completion(1), **Then** the task's completed field becomes True, confirmation message "✓ Task #1 marked as complete" is displayed, and updated task dictionary is returned
2. **Given** a task exists with ID 2 and completed=True, **When** user calls toggle_task_completion(2), **Then** the task's completed field becomes False, confirmation message "✓ Task #2 marked as incomplete" is displayed, and updated task dictionary is returned
3. **Given** a task exists with ID 3, **When** user toggles completion twice, **Then** the task returns to its original completion state (False→True→False or True→False→True)
4. **Given** a task exists with ID 4, **When** user toggles completion, **Then** all other task fields (title, description, created_at) remain unchanged

---

### User Story 2 - Handle Invalid Task IDs (Priority: P2)

As a user, I want to receive a clear error message when I try to toggle completion for a non-existent task ID so I can correct my mistake without confusion.

**Why this priority**: Error handling is essential for user experience but secondary to core functionality. Users need clear feedback when they make mistakes, but this can be implemented after the basic toggle functionality works. This enables graceful degradation and prevents system crashes.

**Independent Test**: Can be tested by calling toggle_task_completion() with an ID that doesn't exist (e.g., 999) and verifying an error message "✗ Error: Task #999 not found" is displayed and a ValueError is raised. No state changes occur.

**Acceptance Scenarios**:

1. **Given** no task exists with ID 999, **When** user calls toggle_task_completion(999), **Then** error message "✗ Error: Task #999 not found" is displayed and ValueError is raised
2. **Given** no task exists with ID 0, **When** user calls toggle_task_completion(0), **Then** error message "✗ Error: Task #0 not found" is displayed and ValueError is raised
3. **Given** tasks exist with IDs 1, 2, 3, **When** user calls toggle_task_completion(4), **Then** error message displays and no tasks are modified
4. **Given** no tasks exist in storage, **When** user calls toggle_task_completion(1), **Then** error message displays indicating task not found

---

### Edge Cases

- What happens when the same task is toggled multiple times rapidly (e.g., 10 times in a row)?
- How does the system handle negative task IDs (e.g., -1)?
- What happens when toggle is called with None as task_id?
- How does the system behave when the storage is empty (no tasks exist)?
- What happens if the task was manually modified between creation and toggle?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task ID (integer) as input to the toggle_task_completion() function
- **FR-002**: System MUST validate that the task ID exists in storage before attempting to toggle
- **FR-003**: System MUST toggle the completed field between False and True (if False→True, if True→False)
- **FR-004**: System MUST display confirmation message "✓ Task #{id} marked as complete" when toggling from False to True
- **FR-005**: System MUST display confirmation message "✓ Task #{id} marked as incomplete" when toggling from True to False
- **FR-006**: System MUST return a dictionary containing all task attributes (id, title, description, completed, created_at) after successful toggle
- **FR-007**: System MUST preserve all non-completed task fields during toggle (title, description, created_at, id remain unchanged)
- **FR-008**: System MUST display error message "✗ Error: Task #{id} not found" when task ID doesn't exist
- **FR-009**: System MUST raise ValueError when task ID doesn't exist (no task modification occurs)
- **FR-010**: System MUST handle the case where storage is empty (no tasks exist) and display appropriate error message

### Key Entities

- **Task**: Existing entity from 001-add-task feature
  - **Attributes**: id (int), title (str), description (str | None), completed (bool), created_at (datetime)
  - **Modified field**: `completed` - toggled between True and False
  - **Immutable fields during toggle**: id, title, description, created_at

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can toggle any existing task's completion status in a single function call
  - **Validation method**: Create task, call toggle_task_completion(id), verify completed field changed and appropriate message displayed

- **SC-002**: System correctly toggles completion status bidirectionally (False→True and True→False)
  - **Validation method**: Create task (starts False), toggle once (becomes True), toggle again (becomes False), verify both transitions work

- **SC-003**: System displays appropriate confirmation message based on new completion status (complete vs incomplete)
  - **Validation method**: Capture output during toggle operations and verify message matches new state

- **SC-004**: All non-completion task fields remain unchanged after toggle operation
  - **Validation method**: Create task, record all field values, toggle completion, verify id/title/description/created_at are identical

- **SC-005**: System handles non-existent task IDs gracefully with clear error messages and no state corruption
  - **Validation method**: Call toggle_task_completion with invalid ID, verify error message displays, confirm ValueError raised, verify no tasks modified

- **SC-006**: Toggle operation completes in under 10ms for typical use cases
  - **Validation method**: Time the toggle_task_completion() function call, verify average execution time < 10ms

### User Experience Goals

- Users receive immediate visual feedback on successful toggle (confirmation message)
- Users receive clear error messages when attempting invalid operations
- Function signature is simple and intuitive (single parameter: task_id)
- Dual output pattern maintained (console message + return value) for consistency with add_task feature

## Assumptions

- This feature builds on the 001-add-task foundation and assumes tasks already exist in storage
- Task IDs are positive integers starting from 1 (per 001-add-task implementation)
- In-memory storage architecture from 001-add-task is used (module-level list)
- Python 3.13+ union type syntax is used per ADR-0001
- System follows the dual output pattern (print + return) established in add_task per FR-007 in 001-add-task
- No authentication or authorization required (single-user system)
- No persistence layer (in-memory only per constitution)
- Local system timezone is used for created_at timestamps (no timezone conversion)

## Dependencies

- **001-add-task**: This feature requires the foundational task management infrastructure:
  - Task dataclass definition (src/models.py)
  - In-memory storage (_tasks list in src/storage.py)
  - Task ID generation system
- **Python 3.13+**: For union type syntax (str | None)
- **Python standard library**: datetime (already used in 001-add-task)

## Out of Scope

- Batch toggle operations (toggling multiple tasks at once)
- Partial completion (progress percentage) - only binary complete/incomplete states
- Completion timestamps (tracking when task was completed)
- Task history or audit log of completion status changes
- Undo/redo functionality for toggle operations
- Search or filter tasks by completion status (separate feature)
- Persistence of task data (remains in-memory only)
- User authentication or multi-user support
- REST API or web interface (CLI/function-level interface only)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Task ID doesn't exist | High | Low | Validate task existence before toggle, raise ValueError with clear message (FR-009) |
| Multiple rapid toggles cause state confusion | Medium | Low | Each toggle is atomic operation, no async complexity |
| Storage becomes out of sync | Low | Medium | Use module-level storage with direct reference updates (consistent with 001-add-task) |
| Performance degradation with large task lists | Low | Low | Linear search is acceptable for prototype, can optimize if needed |

## Future Enhancements (Not in This Feature)

- Add completion_date field to track when tasks were marked complete
- Support filtering/searching tasks by completion status
- Add bulk toggle operations (toggle multiple tasks)
- Add completion statistics (e.g., "You've completed 15 out of 20 tasks")
- Support task completion history/audit trail
- Add undo functionality for accidental toggles
