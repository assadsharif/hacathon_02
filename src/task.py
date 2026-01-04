"""Task data model and storage."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Task data structure.

    Attributes:
        id: Unique task identifier
        title: Task title (required)
        description: Optional task description
        completed: Task completion status
        created_at: Timestamp of task creation
    """
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
