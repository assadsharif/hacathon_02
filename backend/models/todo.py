"""
[Task]: AUTH-A1 (refactor existing Todo model)
[Task]: T013 - Extended with Phase V fields
[From]: Migrating models.py to models/ package structure

Todo Model - SQLModel table definition

This model mirrors the Phase I Todo domain logic with database persistence.
Extended in Phase V with advanced task features.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from typing import Optional, Literal
import uuid


class Todo(SQLModel, table=True):
    """
    Todo table model.

    This model mirrors the Phase I Todo domain logic with database persistence.
    All fields and behavior should match Phase I specifications.

    [Task]: AUTH-A2 - Added user_id for user-scoped data
    [Task]: T013 - Extended with Phase V fields (priority, due_date, recurrence, etc.)

    Table: todos

    Fields (Phase II):
        id: Primary key, auto-incremented
        user_id: Foreign key to users table (owner of todo)
        title: Todo title (required, max 200 characters)
        description: Optional task description (Phase I compatibility)
        status: Todo status ("active" or "completed")
        created_at: Timestamp when todo was created
        updated_at: Timestamp when todo was last updated

    Fields (Phase V - NEW):
        priority: Task priority (low, medium, high)
        due_date: When task is due
        reminder_at: When to send reminder
        recurrence_rule: Recurrence pattern (daily, weekly, monthly)
        recurrence_interval: Repeat every N periods
        recurrence_end_date: When recurrence stops
        parent_task_id: For recurring task instances
    """

    __tablename__ = "todos"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the todo"
    )

    # Foreign key to users table
    # [Task]: AUTH-A2 - User association for data isolation
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True),
        description="User ID (owner of this todo)"
    )

    # Title field
    title: str = Field(
        max_length=200,
        min_length=1,
        description="Todo title (1-200 characters)"
    )

    # Description field (optional, mirrors Phase I)
    description: Optional[str] = Field(
        default=None,
        description="Optional task description (Phase I compatibility)"
    )

    # Status field (must be "active" or "completed")
    status: str = Field(
        default="active",
        max_length=20,
        description="Todo status: 'active' or 'completed'"
    )

    # === Phase V Fields (NEW) ===

    # Priority field (low, medium, high)
    priority: str = Field(
        default="medium",
        max_length=10,
        description="Task priority: 'low', 'medium', or 'high'"
    )

    # Due date for task deadlines
    due_date: Optional[datetime] = Field(
        default=None,
        description="When task is due"
    )

    # Reminder time
    reminder_at: Optional[datetime] = Field(
        default=None,
        description="When to send reminder notification"
    )

    # Recurrence rule (daily, weekly, monthly)
    recurrence_rule: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Recurrence pattern: 'daily', 'weekly', 'monthly', or null"
    )

    # Recurrence interval (repeat every N periods)
    recurrence_interval: int = Field(
        default=1,
        ge=1,
        description="Repeat every N periods (default: 1)"
    )

    # Recurrence end date
    recurrence_end_date: Optional[datetime] = Field(
        default=None,
        description="When recurrence stops (null = infinite)"
    )

    # Parent task ID for recurring instances
    parent_task_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("todos.id"), nullable=True),
        description="Parent task ID for recurring task instances"
    )

    # === Timestamp fields ===

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when todo was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when todo was last updated"
    )

    def __repr__(self) -> str:
        """String representation of Todo"""
        return f"Todo(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')"

    @property
    def is_recurring(self) -> bool:
        """Check if this task is a recurring task."""
        return self.recurrence_rule is not None

    @property
    def has_reminder(self) -> bool:
        """Check if this task has a reminder set."""
        return self.reminder_at is not None

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete Phase V implementation",
                "description": "Add event-driven architecture",
                "status": "active",
                "priority": "high",
                "due_date": "2026-01-25T12:00:00Z",
                "recurrence_rule": "weekly",
                "recurrence_interval": 1
            }
        }
