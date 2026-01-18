"""Task management functions for task management features.

This module provides task management functions:
- add_task(): Add new tasks (001-add-task)
- delete_task(): Delete tasks by ID (003-delete-task)
- toggle_task_completion(): Toggle task completion status (002-mark-complete)
- update_task(): Update task title and/or description (001-update-task)

Functions follow dual output pattern (print + return) per specifications.
"""
from datetime import datetime
from typing import Any
from src.models import Task
from src.storage import _tasks, _generate_task_id

# Sentinel value to detect unset parameters in update_task()
_UNSET = object()


def add_task(title: str, description: str | None = None) -> dict[str, Any]:
    """Add a new task to the in-memory task list.

    Implements FR-001 through FR-010 from specs/001-add-task/spec.md.
    Provides dual output per FR-007:
    - Prints confirmation message to stdout
    - Returns dictionary with task details

    Args:
        title: The task title (required, non-empty after stripping whitespace)
        description: Optional task description (can be None)

    Returns:
        Dictionary containing task details:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If title is None, empty string, or whitespace-only

    Examples:
        >>> task = add_task("Buy groceries")
        ✓ Task #1 added: Buy groceries
        >>> print(task['id'])
        1

        >>> task = add_task("Write report", "Q4 performance report")
        ✓ Task #2 added: Write report
        >>> print(task['description'])
        'Q4 performance report'
    """
    # FR-002: Validate title not None or empty after stripping whitespace
    if title is None or not title.strip():
        # FR-008: Display error message to stdout before raising
        print("✗ Error: Task title is required")
        # FR-009: Do not create task when validation fails
        raise ValueError("Task title is required")

    # FR-004: Generate unique sequential ID
    task_id = _generate_task_id()

    # FR-010: Record exact timestamp when task is created
    created_at = datetime.now()

    # FR-005: Create Task with all required attributes
    task = Task(
        id=task_id,
        title=title.strip(),  # Strip whitespace from title
        description=description,
        completed=False,  # Default to False per FR-005
        created_at=created_at
    )

    # FR-006: Store task in memory (append to _tasks list)
    _tasks.append(task)

    # FR-007: Print confirmation message to stdout
    print(f"✓ Task #{task.id} added: {task.title}")

    # FR-007: Return task as dictionary for programmatic access
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }


def delete_task(task_id: int) -> dict[str, Any]:
    """Delete a task by its ID, removing it permanently from storage.

    Implements FR-001 through FR-010 from specs/003-delete-task/spec.md.
    Provides dual output per FR-006:
    - Prints confirmation message to stdout
    - Returns dictionary with task details before deletion

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary containing all task fields before deletion:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If task with given ID does not exist

    Side Effects:
        Removes task from storage permanently (no undo)
        Prints confirmation message: "✓ Task #{id} deleted: {title}"

    Examples:
        >>> task = add_task("Task to delete")
        ✓ Task #1 added: Task to delete
        >>> deleted = delete_task(1)
        ✓ Task #1 deleted: Task to delete
        >>> print(deleted['title'])
        'Task to delete'
    """
    # FR-002: Find task by ID (linear search through _tasks list)
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    # FR-008: Handle task not found
    if task is None:
        # FR-007: Display error message to stdout
        print(f"✗ Error: Task #{task_id} not found")
        # FR-008: Raise ValueError
        raise ValueError(f"Task #{task_id} not found")

    # FR-004: Capture all task fields BEFORE deletion (for return value and audit trail)
    deleted_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }

    # FR-003: Remove task from storage permanently
    _tasks.remove(task)

    # FR-006: Print confirmation message to stdout
    print(f"✓ Task #{task.id} deleted: {task.title}")

    # FR-005: Return captured task dictionary
    return deleted_data


def toggle_task_completion(task_id: int) -> dict[str, Any]:
    """Toggle a task's completion status between True and False.

    Implements FR-001 through FR-010 from specs/002-mark-complete/spec.md.
    Provides dual output per FR-004 and FR-005:
    - Prints status-appropriate confirmation message to stdout
    - Returns dictionary with all task fields after toggle

    Args:
        task_id: The ID of the task to toggle

    Returns:
        Dictionary containing all task fields after toggle:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,  # Toggled value
            'created_at': datetime
        }

    Raises:
        ValueError: If task with given ID does not exist

    Side Effects:
        Toggles task.completed field in storage (False↔True)
        Prints confirmation message: "✓ Task #{id} marked as complete/incomplete"

    Examples:
        >>> task = add_task("Task to complete")
        ✓ Task #1 added: Task to complete
        >>> toggled = toggle_task_completion(1)
        ✓ Task #1 marked as complete
        >>> print(toggled['completed'])
        True
        >>> toggled_again = toggle_task_completion(1)
        ✓ Task #1 marked as incomplete
        >>> print(toggled_again['completed'])
        False
    """
    # FR-002: Find task by ID (linear search through _tasks list)
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    # FR-009: Handle task not found (validation before toggle)
    if task is None:
        # FR-008: Display error message to stdout
        print(f"✗ Error: Task #{task_id} not found")
        # FR-009: Raise ValueError
        raise ValueError(f"Task #{task_id} not found")

    # FR-003: Toggle the completed field bidirectionally
    task.completed = not task.completed

    # FR-004 and FR-005: Display status-appropriate confirmation message
    if task.completed:
        # Task transitioned from False to True
        print(f"✓ Task #{task.id} marked as complete")
    else:
        # Task transitioned from True to False
        print(f"✓ Task #{task.id} marked as incomplete")

    # FR-006: Return dictionary with all task fields (FR-007: all fields preserved)
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }


def update_task(
    task_id: int,
    *,
    title: str | None = _UNSET,
    description: str | None = _UNSET
) -> dict[str, Any]:
    """Update an existing task's title and/or description.

    Implements FR-001 through FR-015 from specs/001-update-task/spec.md.
    Provides dual output per established pattern:
    - Prints confirmation message to stdout (or error message on failure)
    - Returns dictionary with all task attributes (or raises ValueError on failure)

    Implementation Note:
    Uses sentinel value (_UNSET) to distinguish between "parameter not provided"
    vs "parameter explicitly set to None". This allows description=None to clear
    the description while still detecting when no parameters are provided at all.

    Args:
        task_id: The ID of the task to update (required, must exist in storage)
        title: New title for the task (optional, must be non-empty after stripping if provided)
        description: New description for the task (optional, can be None to clear description)

    Returns:
        Dictionary containing all task attributes:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If no fields provided, task ID not found, or title is empty/whitespace-only

    Side Effects:
        Modifies task in _tasks list in-place (updates specified fields only)
        Prints confirmation message: "✓ Task #{id} updated successfully"
        Prints error message on failure: "✗ Error: {specific error}"

    Examples:
        >>> task = add_task("Original Title", "Original Description")
        ✓ Task #1 added: Original Title

        >>> updated = update_task(1, title="New Title")
        ✓ Task #1 updated successfully
        >>> print(updated['title'])
        'New Title'
        >>> print(updated['description'])
        'Original Description'

        >>> updated = update_task(1, description="New Description")
        ✓ Task #1 updated successfully

        >>> updated = update_task(1, title="Both", description="Updated")
        ✓ Task #1 updated successfully

        >>> update_task(1, description=None)
        ✓ Task #1 updated successfully
        # Description is now None (cleared)

        >>> update_task(999, title="New")
        ✗ Error: Task #999 not found
        ValueError: Task #999 not found

        >>> update_task(1, title="")
        ✗ Error: Task title cannot be empty
        ValueError: Task title cannot be empty

        >>> update_task(1)
        ✗ Error: No fields to update
        ValueError: No fields to update
    """
    # FR-004: Validate at least one field provided (VALIDATION 1: cheapest check first)
    if title is _UNSET and description is _UNSET:
        # FR-013: Display error message
        print("✗ Error: No fields to update")
        # FR-014: Raise ValueError
        raise ValueError("No fields to update")

    # FR-003: Find task by ID (VALIDATION 2: task existence check)
    task = None
    for t in _tasks:
        if t.id == task_id:
            task = t
            break

    if task is None:
        # FR-011: Display error message for non-existent task
        print(f"✗ Error: Task #{task_id} not found")
        # FR-014: Raise ValueError
        raise ValueError(f"Task #{task_id} not found")

    # FR-005, FR-015: Validate title non-empty if provided (VALIDATION 3: field-specific check)
    if title is not _UNSET:
        # Title parameter was explicitly provided by caller
        # Check if title is a valid non-empty string or invalid (None/"")
        if title is not None:
            # Title is a string - strip whitespace and validate non-empty
            title_stripped = title.strip()
            if not title_stripped:
                # FR-012: Empty string or whitespace-only is invalid
                print("✗ Error: Task title cannot be empty")
                # FR-014: Raise ValueError
                raise ValueError("Task title cannot be empty")
            # FR-006, FR-015: Update title with whitespace stripped
            task.title = title_stripped
        else:
            # FR-012: title=None provided explicitly is invalid (can't set title to None)
            print("✗ Error: Task title cannot be empty")
            raise ValueError("Task title cannot be empty")

    # FR-006, FR-008: Update description if provided (can be None to clear)
    if description is not _UNSET:
        task.description = description

    # FR-007: Immutable fields (id, completed, created_at) NOT touched - preserved automatically

    # FR-009: Print confirmation message
    print(f"✓ Task #{task_id} updated successfully")

    # FR-010: Return dictionary with all task fields
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }
