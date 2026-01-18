"""
Pydantic Schemas for Request/Response Validation

This module defines the Pydantic models used for API request validation
and response serialization. These are separate from database models to
provide clear API contracts and validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional
import uuid


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

    Example:
        {
            "title": "Complete Phase II implementation",
            "description": "Add description field for Phase I compatibility",
            "status": "active"
        }
    """

    pass


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo.

    All fields are optional - only provided fields will be updated.
    Used in PUT /api/todos/{id} endpoint.

    Example:
        {
            "title": "Updated title",
            "description": "Updated description",
            "status": "completed"
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


class TodoResponse(TodoBase):
    """
    Schema for todo responses.

    Used in GET /api/todos and GET /api/todos/{id} responses.
    Includes all fields including id, user_id, and timestamps.

    [Task]: AUTH-B4 - Added user_id to response schema for user-scoped data

    Example:
        {
            "id": 1,
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete Phase II implementation",
            "status": "active",
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
                "created_at": "2026-01-11T12:00:00",
                "updated_at": "2026-01-11T12:00:00"
            }
        }


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
