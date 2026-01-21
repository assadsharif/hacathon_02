"""
Pydantic Schemas for Request/Response Validation

This module defines the Pydantic models used for API request validation
and response serialization. These are separate from database models to
provide clear API contracts and validation.

[Task]: T017, T019, T020 - Extended with Phase V fields
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal, Optional, List
import uuid


class RecurrenceSchema(BaseModel):
    """Schema for recurrence configuration (Phase V)."""
    rule: Literal["daily", "weekly", "monthly"]
    interval: int = Field(default=1, ge=1)
    end_date: Optional[datetime] = None


class TodoBase(BaseModel):
    """
    Base Todo schema with common fields.

    This is used as a base class for other Todo schemas.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Todo title (1-200 characters)",
        examples=["Complete Phase II implementation"]
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional task description (Phase I compatibility)",
        examples=["Add description field for Phase I compatibility"]
    )
    status: Literal["active", "completed"] = Field(
        default="active",
        description="Todo status: 'active' or 'completed'"
    )


class TodoCreate(TodoBase):
    """
    Schema for creating a new todo.

    Used in POST /api/todos endpoint.
    [Task]: T019 - Extended with Phase V fields

    Example:
        {
            "title": "Complete Phase II implementation",
            "description": "Add description field for Phase I compatibility",
            "status": "active",
            "priority": "high",
            "due_date": "2026-01-25T12:00:00Z",
            "tags": ["work", "important"]
        }
    """
    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Task priority"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="When task is due"
    )
    reminder_at: Optional[datetime] = Field(
        default=None,
        description="When to send reminder notification"
    )
    recurrence: Optional[RecurrenceSchema] = Field(
        default=None,
        description="Recurrence configuration"
    )
    tags: List[str] = Field(
        default_factory=list,
        max_length=10,
        description="Tag names to associate (max 10)"
    )

    @field_validator("reminder_at")
    @classmethod
    def reminder_before_due(cls, v, info):
        """[Task]: T020 - Validate that reminder is before or equal to due_date."""
        if v and info.data.get("due_date"):
            if v > info.data["due_date"]:
                raise ValueError("reminder_at must be before or equal to due_date")
        return v


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo.

    All fields are optional - only provided fields will be updated.
    Used in PUT /api/todos/{id} endpoint.
    [Task]: T019 - Extended with Phase V fields

    Example:
        {
            "title": "Updated title",
            "description": "Updated description",
            "status": "completed",
            "priority": "high",
            "tags": ["urgent"]
        }
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated todo title"
    )
    description: Optional[str] = Field(
        None,
        description="Updated todo description"
    )
    status: Optional[Literal["active", "completed"]] = Field(
        None,
        description="Updated todo status"
    )
    priority: Optional[Literal["low", "medium", "high"]] = Field(
        None,
        description="Updated priority"
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Updated due date"
    )
    reminder_at: Optional[datetime] = Field(
        None,
        description="Updated reminder time"
    )
    recurrence: Optional[RecurrenceSchema] = Field(
        None,
        description="Updated recurrence configuration"
    )
    tags: Optional[List[str]] = Field(
        None,
        max_length=10,
        description="Updated tags (max 10)"
    )


class TodoResponse(TodoBase):
    """
    Schema for todo responses.

    Used in GET /api/todos and GET /api/todos/{id} responses.
    Includes all fields including id, user_id, and timestamps.

    [Task]: AUTH-B4 - Added user_id to response schema for user-scoped data
    [Task]: T019 - Extended with Phase V fields

    Example:
        {
            "id": 1,
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete Phase II implementation",
            "status": "active",
            "priority": "high",
            "due_date": "2026-01-25T12:00:00Z",
            "tags": ["work", "important"],
            "created_at": "2026-01-11T12:00:00",
            "updated_at": "2026-01-11T12:00:00"
        }
    """

    id: int = Field(
        ...,
        description="Unique identifier"
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        description="User ID (owner of this todo) - UUID"
    )
    priority: str = Field(
        default="medium",
        description="Task priority"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="When task is due"
    )
    reminder_at: Optional[datetime] = Field(
        default=None,
        description="When to send reminder"
    )
    recurrence: Optional[RecurrenceSchema] = Field(
        default=None,
        description="Recurrence configuration"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Associated tag names"
    )
    parent_task_id: Optional[int] = Field(
        default=None,
        description="Parent task ID for recurring instances"
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp"
    )

    class Config:
        """Pydantic configuration"""
        from_attributes = True  # Allow creation from SQLModel objects
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete Phase II implementation",
                "description": "Add description field for Phase I compatibility",
                "status": "active",
                "priority": "high",
                "due_date": "2026-01-25T12:00:00Z",
                "tags": ["work", "important"],
                "created_at": "2026-01-11T12:00:00",
                "updated_at": "2026-01-11T12:00:00"
            }
        }


class TodoListResponse(BaseModel):
    """
    Schema for paginated todo list response.
    [Task]: T017 - Pagination support
    """
    items: List[TodoResponse]
    total: int
    page: int
    limit: int
    pages: int


class ErrorResponse(BaseModel):
    """
    Schema for error responses.

    Used for consistent error formatting across all endpoints.

    Example:
        {
            "detail": "Todo not found"
        }
    """

    detail: str = Field(
        ...,
        description="Error message",
        examples=["Todo not found"]
    )
