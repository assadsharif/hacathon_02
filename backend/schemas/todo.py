"""
[Task]: T019
Todo Schemas - Pydantic models for todo API requests/responses

Phase V: Event-Driven Architecture
Extended with priority, due_date, recurrence, and tags
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime


class RecurrenceSchema(BaseModel):
    """Schema for recurrence configuration."""
    rule: Literal["daily", "weekly", "monthly"]
    interval: int = Field(default=1, ge=1)
    end_date: Optional[datetime] = None


class TodoBase(BaseModel):
    """Base schema for todo data."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TodoCreate(TodoBase):
    """Schema for creating a todo."""
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    recurrence: Optional[RecurrenceSchema] = None
    tags: List[str] = Field(default_factory=list, max_length=10)

    @field_validator("reminder_at")
    @classmethod
    def reminder_before_due(cls, v, info):
        """Validate that reminder is before or equal to due_date."""
        if v and info.data.get("due_date"):
            if v > info.data["due_date"]:
                raise ValueError("reminder_at must be before or equal to due_date")
        return v


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[Literal["active", "completed"]] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    recurrence: Optional[RecurrenceSchema] = None
    tags: Optional[List[str]] = Field(None, max_length=10)


class TodoResponse(TodoBase):
    """Schema for todo response."""
    id: int
    status: str
    priority: str
    due_date: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    recurrence: Optional[RecurrenceSchema] = None
    tags: List[str] = []
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for paginated todo list response."""
    items: List[TodoResponse]
    total: int
    page: int
    limit: int
    pages: int


class TodoFilterParams(BaseModel):
    """Schema for todo filtering parameters."""
    status: Optional[Literal["active", "completed", "all"]] = "all"
    priority: Optional[Literal["low", "medium", "high"]] = None
    tag: Optional[str] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    search: Optional[str] = None
    sort: Literal["created_at", "due_date", "priority", "title"] = "created_at"
    order: Literal["asc", "desc"] = "desc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
