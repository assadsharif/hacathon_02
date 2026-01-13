"""Task data models for 001-add-task feature.

This module defines the core Task dataclass following the specification
at specs/001-add-task/spec.md and ADR-0001 (union type syntax).
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Represents a task in the todo list.

    Attributes:
        id: Unique sequential identifier (assigned by storage layer)
        title: Task title (required, non-empty after stripping whitespace)
        description: Optional detailed description (can be None)
        completed: Completion status (default: False)
        created_at: Creation timestamp (system local time, timezone-naive)
    """
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
