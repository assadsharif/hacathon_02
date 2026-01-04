"""Task data models.

This module defines the core data structures for the Todo application,
following the specification at /specs/phase1/features/add-task.md.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Task data model.

    Represents a todo task with all required fields as per AC4.

    Attributes:
        id: Unique task identifier (auto-assigned, starts from 1)
        title: Task title (required, non-empty string)
        description: Optional task description (can be None)
        completed: Task completion status (default: False)
        created_at: Timestamp when the task was created
    """
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert Task to dictionary representation.

        Returns:
            Dictionary with all task fields
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }
