"""Task management functions."""
from datetime import datetime
from typing import Any

from .task import Task


# Global in-memory task storage
tasks: list[Task] = []

# Task ID counter
_task_id_counter: int = 0


def add_task(title: str, description: str | None = None) -> dict[str, Any]:
    """Add a new task to the in-memory task list.

    Args:
        title: The task title (required, non-empty)
        description: Optional task description

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
        ValueError: If title is empty or None
    """
    global _task_id_counter

    # Validate title
    if title is None or (isinstance(title, str) and title.strip() == ""):
        raise ValueError("Task title is required")

    # Increment ID counter
    _task_id_counter += 1

    # Create task
    task = Task(
        id=_task_id_counter,
        title=title.strip(),
        description=description,
        completed=False,
        created_at=datetime.now()
    )

    # Store in memory
    tasks.append(task)

    # Return task as dictionary
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }


def get_all_tasks() -> list[Task]:
    """Retrieve all tasks from in-memory storage.

    Returns:
        List of all tasks
    """
    return tasks.copy()


def clear_all_tasks() -> None:
    """Clear all tasks from in-memory storage.

    Used primarily for testing.
    """
    global _task_id_counter
    tasks.clear()
    _task_id_counter = 0
