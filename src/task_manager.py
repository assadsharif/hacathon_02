"""Task management functions for task management features.

This module provides task management functions:
- add_task(): Add new tasks (001-add-task)
- delete_task(): Delete tasks by ID (003-delete-task)

Functions follow dual output pattern (print + return) per specifications.
"""
from datetime import datetime
from typing import Any
from src.models import Task
from src.storage import _tasks, _generate_task_id


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
