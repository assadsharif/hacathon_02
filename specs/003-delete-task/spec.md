# Feature Specification: Delete Task by ID

**Feature Branch**: `003-delete-task`
**Created**: 2026-01-13
**Status**: Draft
**Input**: User description: "Convert delete-task feature from Phase I spec. User story: As a user, I want to delete a task by its ID so I can remove tasks I no longer need from my list. Key requirements: (1) Accept task ID as input, (2) Remove task from storage permanently, (3) Return deleted task dictionary for confirmation, (4) Display confirmation message with task details, (5) Handle non-existent task IDs with clear error. Technical: Function signature delete_task(task_id: int) -> dict[str, Any]. Delete behavior: Find task by ID, remove from _tasks list, return task data before deletion. Confirmation message: '✓ Task #{id} deleted: {title}'. Error: '✗ Error: Task #{id} not found' when ID doesn't exist. Deletion is permanent (no undo). All task fields should be in the return dictionary for logging/audit purposes. Builds on 001-add-task and 002-mark-complete foundation (reuses task lookup and error handling patterns)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Delete Task by ID (Priority: P1)

As a user, I want to delete a task by its ID so I can remove tasks I no longer need from my task list, keeping my list clean and focused on relevant work.

**Why this priority**: This is the core deletion functionality that completes the CRUD operations for task management. Without the ability to delete tasks, users cannot remove completed, cancelled, or irrelevant tasks, leading to cluttered task lists. This is essential for maintaining a usable task management system and represents the minimum viable product for this feature.

**Independent Test**: Can be fully tested by creating a task with add_task(), calling delete_task() with the task ID, and verifying the task is removed from storage, the deleted task dictionary is returned with all fields, and the confirmation message displays. Delivers immediate value by allowing users to clean up their task lists.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1, **When** user calls delete_task(1), **Then** the task is removed from storage, all task fields are returned in a dictionary, and confirmation message "✓ Task #1 deleted: {title}" is displayed
2. **Given** tasks exist with IDs 1, 2, 3, **When** user calls delete_task(2), **Then** only task #2 is removed from storage, tasks #1 and #3 remain unchanged
3. **Given** a task exists with ID 5, **When** user calls delete_task(5), **Then** the returned dictionary contains all task fields (id, title, description, completed, created_at) exactly as they were before deletion
4. **Given** multiple tasks exist, **When** user deletes a task, **Then** other tasks remain accessible with their original IDs and all fields unchanged

---

### User Story 2 - Handle Invalid Delete Attempts (Priority: P2)

As a user, I want to receive a clear error message when I try to delete a non-existent task ID so I understand why the operation failed and can correct my mistake without confusion.

**Why this priority**: Error handling is essential for user experience but secondary to core deletion functionality. Users need clear feedback when they make mistakes (typos in ID, attempting to delete already-deleted tasks), but this can be implemented after the basic delete functionality works. This enables graceful degradation and prevents system crashes.

**Independent Test**: Can be tested by calling delete_task() with an ID that doesn't exist (e.g., 999) and verifying an error message "✗ Error: Task #999 not found" is displayed, a ValueError is raised, and no tasks in storage are modified.

**Acceptance Scenarios**:

1. **Given** no task exists with ID 999, **When** user calls delete_task(999), **Then** error message "✗ Error: Task #999 not found" is displayed and ValueError is raised
2. **Given** tasks exist with IDs 1, 2, 3, **When** user calls delete_task(5), **Then** error message displays, ValueError is raised, and tasks 1, 2, 3 remain unchanged in storage
3. **Given** a task with ID 1 was already deleted, **When** user calls delete_task(1) again, **Then** error message displays indicating task not found
4. **Given** no tasks exist in storage, **When** user calls delete_task(1), **Then** error message displays indicating task not found

---

### Edge Cases

- What happens when deleting the only task in the list (storage becomes empty)?
- What happens when deleting the first task when multiple tasks exist (index 0)?
- What happens when deleting the last task when multiple tasks exist (final index)?
- What happens when deleting a middle task (other tasks should maintain their positions)?
- How does the system handle negative task IDs (e.g., -1)?
- What happens when delete is called with None as task_id?
- How does deletion affect subsequent add_task() calls (new IDs should not reuse deleted IDs)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task ID (integer) as input to the delete_task() function
- **FR-002**: System MUST validate that the task ID exists in storage before attempting to delete
- **FR-003**: System MUST remove the task from storage permanently (no undo or soft delete)
- **FR-004**: System MUST capture all task fields (id, title, description, completed, created_at) BEFORE deletion for return value
- **FR-005**: System MUST return a dictionary containing all deleted task attributes after successful deletion
- **FR-006**: System MUST display confirmation message "✓ Task #{id} deleted: {title}" after successful deletion
- **FR-007**: System MUST display error message "✗ Error: Task #{id} not found" when task ID doesn't exist
- **FR-008**: System MUST raise ValueError when task ID doesn't exist (no task modification occurs)
- **FR-009**: System MUST ensure that deletion of one task does not affect other tasks in storage (IDs, content, order preserved)
- **FR-010**: System MUST handle the case where storage is empty (no tasks exist) and display appropriate error message

### Key Entities

- **Task**: Existing entity from 001-add-task feature
  - **Attributes**: id (int), title (str), description (str | None), completed (bool), created_at (datetime)
  - **Operation**: Removed from storage by delete_task()
  - **Return**: All fields returned in dictionary before deletion for audit/logging purposes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can delete any existing task by ID in a single function call
  - **Validation method**: Create task, call delete_task(id), verify task removed from storage and confirmation message displayed

- **SC-002**: Deleted tasks are permanently removed from storage and cannot be retrieved
  - **Validation method**: Delete task, attempt to access it (e.g., toggle completion, delete again), verify task not found errors

- **SC-003**: System returns complete task information before deletion for audit purposes
  - **Validation method**: Create task with all fields populated, delete it, verify returned dictionary contains id, title, description, completed, created_at with correct values

- **SC-004**: Deletion of one task does not affect other tasks in storage
  - **Validation method**: Create 5 tasks, delete task #3, verify tasks #1, #2, #4, #5 still exist with unchanged content and IDs

- **SC-005**: System handles non-existent task IDs gracefully with clear error messages and no state corruption
  - **Validation method**: Call delete_task with invalid ID, verify error message displays, confirm ValueError raised, verify all existing tasks remain unmodified

- **SC-006**: Delete operation completes in under 10ms for typical use cases
  - **Validation method**: Time the delete_task() function call with 100 tasks in storage, verify average execution time < 10ms

### User Experience Goals

- Users receive immediate visual feedback on successful deletion (confirmation message with task title)
- Users receive clear error messages when attempting invalid operations
- Function signature is simple and intuitive (single parameter: task_id)
- Dual output pattern maintained (console message + return value) for consistency with add_task and toggle_task_completion features
- Deleted task information returned for logging/audit trail purposes

## Assumptions

- This feature builds on the 001-add-task and 002-mark-complete foundation and assumes tasks already exist in storage
- Task IDs are positive integers starting from 1 (per 001-add-task implementation)
- In-memory storage architecture from 001-add-task is used (module-level list)
- Python 3.13+ union type syntax is used per ADR-0001
- System follows the dual output pattern (print + return) established in add_task per FR-007 in 001-add-task
- No authentication or authorization required (single-user system)
- No persistence layer (in-memory only per constitution)
- Deletion is permanent with no undo functionality
- Deleted task IDs are not reused by subsequent add_task() calls (counter only increments)
- Task list order is maintained by list index (deletion may shift indices but doesn't affect task data)

## Dependencies

- **001-add-task**: This feature requires the foundational task management infrastructure:
  - Task dataclass definition (src/models.py)
  - In-memory storage (_tasks list in src/storage.py)
  - Task ID generation system
- **002-mark-complete**: This feature reuses patterns from toggle completion:
  - Task lookup by ID (linear search pattern)
  - Error handling for non-existent IDs (ValueError pattern)
  - Dual output pattern (print + return dictionary)
- **Python 3.13+**: For union type syntax (str | None)
- **Python standard library**: datetime (already used in 001-add-task)

## Out of Scope

- Undo/redo functionality for deletion (tasks are permanently deleted)
- Soft delete or trash/recycle bin (tasks are immediately removed from storage)
- Batch delete operations (deleting multiple tasks at once)
- Delete confirmation prompt ("Are you sure?") - caller responsibility
- Cascade deletion (no dependent entities to clean up)
- Delete history or audit log (only return value provides deleted task data)
- Search or filter before delete (separate feature)
- Persistence of deletion (remains in-memory only)
- User authentication or multi-user support
- REST API or web interface (CLI/function-level interface only)
- Reusing deleted task IDs (IDs increment monotonically, never reused)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Task ID doesn't exist | High | Low | Validate task existence before delete, raise ValueError with clear message (FR-008) |
| Accidental deletion (no undo) | Medium | Medium | Return full task data for manual recovery, document permanent deletion behavior |
| Storage becomes out of sync | Low | Medium | Use module-level storage with direct reference removal (consistent with 001-add-task) |
| Deleting wrong task affects others | Low | High | Test extensively to ensure only target task removed, others preserved |
| Performance degradation with large lists | Low | Low | Linear search is acceptable for prototype, can optimize if needed |

## Future Enhancements (Not in This Feature)

- Add soft delete with trash/recycle bin functionality
- Implement undo/redo for deletions
- Support bulk delete operations (delete multiple tasks)
- Add delete confirmation prompt option
- Add deletion history/audit trail separate from return value
- Support filtering before delete (e.g., "delete all completed tasks")
- Add cascade deletion if dependent entities are introduced
- Implement delete by criteria (e.g., delete by title, date range)
