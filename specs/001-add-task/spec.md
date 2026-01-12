# Feature Specification: Add Task

**Feature Branch**: `001-add-task`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Convert existing add-task feature specification from specs/phase1/features/add-task.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Basic Task (Priority: P1)

As a user, I want to add a new task with just a title to my list so I can quickly capture tasks I need to remember.

**Why this priority**: This is the core functionality - without the ability to add tasks, the system has no value. This is the minimum viable feature.

**Independent Test**: Can be fully tested by creating a task with only a title and verifying it appears in the task list with a unique ID and confirmation message. Delivers immediate value by allowing users to capture tasks.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** I add a task with title "Buy groceries", **Then** the system assigns it ID 1, stores it with completed=False, displays confirmation "✓ Task #1 added: Buy groceries"
2. **Given** a task list with 5 existing tasks, **When** I add a task with title "Call dentist", **Then** the system assigns it the next sequential ID (6), stores it, and displays confirmation

---

### User Story 2 - Add Task with Description (Priority: P2)

As a user, I want to add a task with both a title and description so I can capture additional context and details about what needs to be done.

**Why this priority**: Enhances task capture with optional context. Users can still add tasks without this (P1), but descriptions add value for complex tasks.

**Independent Test**: Can be tested by creating tasks with descriptions and verifying the description is stored and retrievable. Delivers value by allowing richer task information.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** I add a task with title "Write report" and description "Quarterly performance report for Q4", **Then** the system stores both title and description, assigns ID 1, and displays confirmation
2. **Given** a task list, **When** I add a task with title "Review code" and description set to empty string "", **Then** the system accepts the empty description and stores the task successfully

---

### User Story 3 - Handle Invalid Task Input (Priority: P1)

As a user, when I attempt to add a task without a title or with only whitespace, I want to receive clear error feedback so I understand what went wrong and can correct it.

**Why this priority**: Critical for data integrity and user experience. Without validation, the system could have tasks with no meaningful content. Must be implemented alongside P1 story.

**Independent Test**: Can be tested by attempting to create tasks with empty, None, or whitespace-only titles and verifying appropriate error messages appear and no task is created.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** I attempt to add a task with title="" (empty string), **Then** the system displays error "✗ Error: Task title is required" and no task is created
2. **Given** an empty task list, **When** I attempt to add a task with title=None, **Then** the system displays error "✗ Error: Task title is required" and no task is created
3. **Given** an empty task list, **When** I attempt to add a task with title="   " (only whitespace), **Then** the system displays error "✗ Error: Task title is required" after stripping whitespace

---

### Edge Cases

- What happens when a user provides a title with only whitespace characters? System must strip whitespace and validate it's not empty.
- How does the system handle very long titles or descriptions? System accepts any valid Python string without imposed character limits. This follows the principle of not over-engineering; limits can be added later if usage patterns indicate need.
- What happens when the system reaches maximum integer value for task IDs? Assume sequential IDs won't reach limits in realistic usage (documented in Assumptions).
- How does the system handle special characters or Unicode in titles/descriptions? System should accept any valid Python string.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task title as a required string input
- **FR-002**: System MUST validate that task title is not None or empty after stripping whitespace
- **FR-003**: System MUST accept an optional task description as a string or None value
- **FR-004**: System MUST assign each task a unique sequential integer ID starting from 1
- **FR-005**: System MUST store each task with the following attributes: id (int), title (str), description (str | None), completed (bool defaulting to False), created_at (timestamp)
- **FR-006**: System MUST store tasks in memory without persistence to disk or database
- **FR-007**: System MUST provide dual output upon successful task creation:
  - **Console output**: Print confirmation message in format "✓ Task #{id} added: {title}" to stdout
  - **Return value**: Return dictionary containing task details: `{'id': int, 'title': str, 'description': str | None, 'completed': bool, 'created_at': datetime}`
  - **Rationale**: Console output provides immediate user feedback; return value enables programmatic access and testing
- **FR-008**: System MUST display error message "✗ Error: Task title is required" to stdout when title validation fails (before raising ValueError)
- **FR-009**: System MUST NOT create a task when validation fails
- **FR-010**: System MUST record the exact timestamp when each task is created using `datetime.now()` (system local time). Timestamps are stored as timezone-naive `datetime` objects for simplicity in Phase I (console app). Future phases with persistence may add timezone-aware UTC timestamps.

### Key Entities

- **Task**: Represents a single task item with the following attributes:
  - `id`: Unique integer identifier (sequential, starting from 1)
  - `title`: Required string describing the task
  - `description`: Optional string with additional task details (can be None)
  - `completed`: Boolean flag indicating completion status (defaults to False)
  - `created_at`: Timestamp capturing when the task was created

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task with just a title in a single operation with immediate confirmation
  - **Validation Method**: Call `add_task("Test task")`, verify: (1) console prints "✓ Task #1 added: Test task", (2) function returns dictionary with id=1 and title="Test task", (3) task appears in `_tasks` list within <10ms

- **SC-002**: System successfully assigns unique, sequential IDs to all tasks without collisions
  - **Validation Method**: Create 100 tasks in sequence, verify: (1) IDs are 1, 2, 3, ..., 100 with no gaps, (2) no duplicate IDs exist in `_tasks` list, (3) run `assert len(set(t.id for t in _tasks)) == len(_tasks)` to confirm uniqueness

- **SC-003**: 100% of valid task creations (non-empty title) result in successful storage and confirmation message
  - **Validation Method**: Run test suite 100 times with valid inputs (e.g., "Task A", "Task B"), verify: (1) all 100 iterations succeed without exceptions, (2) all 100 tasks appear in `_tasks` list, (3) all 100 confirmation messages printed

- **SC-004**: 100% of invalid task creations (empty/None title) are rejected with clear error message and no task created
  - **Validation Method**: Attempt to create tasks with: (1) empty string "", (2) None, (3) whitespace "   ". Verify for each: ValueError raised with message "Task title is required", error message printed to stdout, no task added to `_tasks` list

- **SC-005**: Users can capture optional task descriptions with any valid string content including empty strings
  - **Validation Method**: Create tasks with: (1) description=None, (2) description="", (3) description="Valid text", (4) description="Unicode: 你好🎉". Verify all succeed and returned dictionary contains exact description value passed

- **SC-006**: All task creation timestamps are accurate to the second
  - **Validation Method**: Record `before = datetime.now()`, call `add_task("Test")`, record `after = datetime.now()`. Verify: (1) `before <= task['created_at'] <= after`, (2) timestamp difference is <1 second, (3) timestamp type is `datetime` object

## Assumptions *(mandatory)*

1. **Runtime Environment**: Tasks are stored in-memory for the duration of the application runtime; data is lost when the application stops
2. **ID Generation**: Sequential integer IDs will not overflow in realistic usage (max int is sufficient for expected task volume)
3. **Concurrency**: Single-threaded operation assumed; no concurrent task creation handled in this phase
4. **String Encoding**: All string inputs (title, description) use standard Python str type with UTF-8 encoding
5. **Validation Scope**: Only title validation is required; descriptions accept any string value including empty strings
6. **User Interface**: Confirmation and error messages are displayed via standard output/print statements
7. **Performance**: In-memory list storage is acceptable for expected task volume (no performance optimization required)

## Dependencies & Constraints *(mandatory)*

### Dependencies

- Python 3.13+ (for union type syntax: `str | None`)
- Python standard library: `dataclasses`, `datetime`
- No external package dependencies

### Constraints

- **Storage**: In-memory only, no file I/O or database operations
- **Data Structure**: Must use Python list for task storage
- **ID Strategy**: Sequential integer IDs only, must start at 1
- **Validation**: Title validation must occur before task creation and ID assignment

## Out of Scope *(mandatory)*

The following capabilities are explicitly excluded from this feature:

- Task persistence to disk, database, or any storage medium
- Task retrieval, listing, or querying functionality
- Task update or modification capabilities
- Task deletion functionality
- Task completion toggling (marking tasks as done/undone)
- Task search, filter, or sort capabilities
- Multi-user support or user authentication
- Concurrent task creation handling
- Task priority or categorization
- Task due dates or reminders
- Batch task operations
- Undo/redo functionality
- Data export or import

## Open Questions

None. All clarifications have been resolved.

