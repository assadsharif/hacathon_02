# Feature Specification: Update Task Details

**Feature Branch**: `001-update-task`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "004-update-task"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update Task Fields (Priority: P1)

As a user, I want to update a task's title and/or description so I can correct mistakes, add more details, or clarify task information as my understanding of the work evolves.

**Why this priority**: This is the core functionality that enables users to maintain accurate and up-to-date task information. Users frequently need to refine task details after initial creation, whether to fix typos, add context discovered during work, or clarify requirements. This is essential for any task management system where tasks evolve over time and represents the minimum viable product for this feature.

**Independent Test**: Can be fully tested by creating a task with add_task(), calling update_task() with the task ID and new field values, and verifying the specified fields are updated while other fields remain unchanged. Delivers immediate value by allowing users to maintain accurate task information.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1, title "Old Title", and description "Old Description", **When** user calls update_task(1, title="New Title"), **Then** the task's title becomes "New Title", description remains "Old Description", confirmation message is displayed, and updated task dictionary is returned
2. **Given** a task exists with ID 2, title "Task 2", and description "Original", **When** user calls update_task(2, description="Updated Description"), **Then** the task's description becomes "Updated Description", title remains "Task 2", confirmation message is displayed, and updated task dictionary is returned
3. **Given** a task exists with ID 3, title "Old", and description "Old", **When** user calls update_task(3, title="New", description="New"), **Then** both title and description are updated, confirmation message is displayed, and updated task dictionary is returned
4. **Given** a task exists with ID 4, **When** user updates the task, **Then** immutable fields (id, completed, created_at) remain unchanged
5. **Given** a task exists with ID 5, **When** user calls update_task(5, description=None), **Then** the task's description becomes None (cleared), and confirmation message is displayed

---

### User Story 2 - Handle Invalid Updates (Priority: P2)

As a user, I want to receive clear error messages when I try to update a task with invalid inputs so I can correct my mistakes without confusion or data corruption.

**Why this priority**: Error handling is essential for data integrity and user experience but secondary to core functionality. Users need clear feedback when they make mistakes (non-existent IDs, invalid field values), but this can be implemented after the basic update functionality works. This prevents data corruption and system crashes.

**Independent Test**: Can be tested by calling update_task() with various invalid inputs (non-existent ID, empty title, no fields to update) and verifying appropriate error messages are displayed and ValueError is raised. No state changes occur.

**Acceptance Scenarios**:

1. **Given** no task exists with ID 999, **When** user calls update_task(999, title="New"), **Then** error message "✗ Error: Task #999 not found" is displayed and ValueError is raised
2. **Given** a task exists with ID 1, **When** user calls update_task(1, title=""), **Then** error message "✗ Error: Task title cannot be empty" is displayed and ValueError is raised, task remains unchanged
3. **Given** a task exists with ID 2, **When** user calls update_task(2) with no field updates, **Then** error message "✗ Error: No fields to update" is displayed and ValueError is raised
4. **Given** a task exists with ID 3, **When** user calls update_task(3, title="   "), **Then** error message about empty title is displayed (whitespace-only treated as empty) and ValueError is raised

---

### Edge Cases

- What happens when updating a task with a very long title (e.g., 1000 characters)?
- How does the system handle special characters in title/description (e.g., emojis, unicode)?
- What happens when update_task is called with None as task_id?
- How does the system handle updating description to None (clearing it)?
- What happens when multiple updates are made to the same task rapidly?
- How does the system behave when the storage is empty (no tasks exist)?
- What happens if both title and description are provided but title is invalid (e.g., empty)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task ID (integer) as the first required parameter to update_task()
- **FR-002**: System MUST accept optional keyword arguments for title (str) and description (str | None)
- **FR-003**: System MUST validate that the task ID exists in storage before attempting to update
- **FR-004**: System MUST validate that at least one field (title or description) is provided for update
- **FR-005**: System MUST validate that title, if provided, is not empty (after stripping whitespace)
- **FR-006**: System MUST update only the specified fields (title and/or description) and preserve all other fields
- **FR-007**: System MUST preserve immutable fields during update: id, completed, created_at
- **FR-008**: System MUST allow description to be set to None (clearing the description)
- **FR-009**: System MUST display confirmation message "✓ Task #{id} updated successfully" after successful update
- **FR-010**: System MUST return a dictionary containing all task attributes after successful update
- **FR-011**: System MUST display error message "✗ Error: Task #{id} not found" when task ID doesn't exist
- **FR-012**: System MUST display error message "✗ Error: Task title cannot be empty" when title is empty or whitespace-only
- **FR-013**: System MUST display error message "✗ Error: No fields to update" when no update fields are provided
- **FR-014**: System MUST raise ValueError when validation fails (non-existent ID, empty title, no fields)
- **FR-015**: System MUST strip leading/trailing whitespace from title if provided

### Key Entities

- **Task**: Existing entity from 001-add-task feature
  - **Attributes**: id (int), title (str), description (str | None), completed (bool), created_at (datetime)
  - **Mutable fields**: title, description
  - **Immutable fields during update**: id, completed, created_at

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update any existing task's title and/or description in a single function call
  - **Validation method**: Create task, call update_task(id, title="New"), verify title changed and confirmation message displayed

- **SC-002**: System correctly updates only specified fields while preserving all other fields
  - **Validation method**: Create task, update only title, verify description/completed/created_at/id unchanged; repeat for description-only update

- **SC-003**: System allows description to be cleared (set to None) while maintaining other fields
  - **Validation method**: Create task with description, update with description=None, verify description is None and other fields unchanged

- **SC-004**: System validates input and rejects empty titles with clear error messages
  - **Validation method**: Attempt to update with empty title ("" or "   "), verify error message displays, confirm ValueError raised, verify task unchanged

- **SC-005**: System handles non-existent task IDs gracefully with clear error messages and no state corruption
  - **Validation method**: Call update_task with invalid ID, verify error message displays, confirm ValueError raised, verify no tasks modified

- **SC-006**: Update operation completes in under 10ms for typical use cases
  - **Validation method**: Time the update_task() function call, verify average execution time < 10ms

### User Experience Goals

- Users receive immediate visual feedback on successful updates (confirmation message)
- Users receive clear, specific error messages when attempting invalid operations
- Function signature supports flexible updates (can update title only, description only, or both)
- Dual output pattern maintained (console message + return value) for consistency with existing features
- Whitespace is automatically cleaned from titles to prevent accidental empty values

## Assumptions

- This feature builds on the 001-add-task foundation and assumes tasks already exist in storage
- Task IDs are positive integers starting from 1 (per 001-add-task implementation)
- In-memory storage architecture from 001-add-task is used (module-level list)
- Python 3.13+ union type syntax is used per project standards
- System follows the dual output pattern (print + return) established in add_task
- No authentication or authorization required (single-user system)
- No persistence layer (in-memory only per constitution)
- Title validation matches add_task behavior (non-empty after stripping)
- Function signature: update_task(task_id: int, *, title: str | _UNSET = _UNSET, description: str | None | _UNSET = _UNSET) -> dict[str, Any]
- Uses sentinel pattern (_UNSET = object()) to distinguish "not provided" from "explicitly None"
- At least one field (title or description) must be provided (both cannot be omitted)
- Updating description to None is valid (clears the description)
- Updating title to None is invalid (title is required to be non-empty string)
- The completed field is not updated by this function (use toggle_task_completion from 002-mark-complete)

## Dependencies

- **001-add-task**: This feature requires the foundational task management infrastructure:
  - Task dataclass definition (src/models.py)
  - In-memory storage (_tasks list in src/storage.py)
  - Task ID generation system
- **Python 3.13+**: For union type syntax (str | None)
- **Python standard library**: datetime (already used in 001-add-task)

## Out of Scope

- Updating completion status (handled by 002-mark-complete feature)
- Updating created_at timestamp (immutable)
- Updating task ID (immutable)
- Batch update operations (updating multiple tasks at once)
- Partial field updates for description (e.g., append text)
- Task history or audit log of changes
- Undo/redo functionality for updates
- Validation of description length or format
- Rich text or markdown formatting in description
- Persistence of task data (remains in-memory only)
- User authentication or multi-user support
- Conflict resolution for concurrent updates
- REST API or web interface (CLI/function-level interface only)

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Task ID doesn't exist | High | Low | Validate task existence before update, raise ValueError with clear message (FR-014) |
| Empty title provided | Medium | Medium | Validate title is non-empty after stripping whitespace, raise ValueError (FR-012) |
| No fields provided for update | Medium | Low | Validate at least one field provided, raise ValueError with clear message (FR-013) |
| Storage becomes out of sync | Low | Medium | Use module-level storage with direct reference updates (consistent with 001-add-task) |
| Performance degradation with large task lists | Low | Low | Linear search is acceptable for prototype, can optimize if needed |
| Whitespace-only title accepted | Medium | Low | Strip whitespace and validate non-empty (FR-015, FR-005) |

## Future Enhancements (Not in This Feature)

- Add update_date or modified_at field to track when tasks were last updated
- Support batch updates (update multiple tasks at once)
- Add validation for maximum title/description length
- Support rich text or markdown formatting in descriptions
- Add task update history/audit trail
- Add undo functionality for accidental updates
- Support field-level timestamps (track when each field was last modified)
- Add conflict detection for concurrent updates (if multi-user support added)
- Support partial description updates (append, prepend, search/replace)
