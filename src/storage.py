"""In-memory task storage for 001-add-task feature.

This module provides module-level storage infrastructure following
ADR-0002 (in-memory list storage) and ADR-0003 (sequential counter IDs).
"""
from src.models import Task

# In-memory task storage (module-level list per ADR-0002)
_tasks: list[Task] = []

# Task ID counter (module-level, starts at 0, increments before assignment per ADR-0003)
_task_id_counter: int = 0


def _generate_task_id() -> int:
    """Generate next sequential task ID.

    Implements increment-before-assign pattern per ADR-0003.
    IDs start from 1 (counter starts at 0, increments before first use).

    Returns:
        Next unique task ID (1, 2, 3, ...)
    """
    global _task_id_counter
    _task_id_counter += 1
    return _task_id_counter
