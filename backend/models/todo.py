"""
[Task]: AUTH-A1 (refactor existing Todo model)
[From]: Migrating models.py to models/ package structure

Todo Model - SQLModel table definition

This model mirrors the Phase I Todo domain logic with database persistence.
All fields and behavior match Phase I specifications.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from typing import Optional
import uuid


class Todo(SQLModel, table=True):
    """
    Todo table model.

    This model mirrors the Phase I Todo domain logic with database persistence.
    All fields and behavior should match Phase I specifications.

    [Task]: AUTH-A2 - Added user_id for user-scoped data

    Table: todos

    Fields:
        id: Primary key, auto-incremented
        user_id: Foreign key to users table (owner of todo)
        title: Todo title (required, max 200 characters)
        description: Optional task description (Phase I compatibility)
        status: Todo status ("active" or "completed")
        created_at: Timestamp when todo was created
        updated_at: Timestamp when todo was last updated
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

    # Timestamp fields
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
        return f"Todo(id={self.id}, title='{self.title}', status='{self.status}')"

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete Phase II implementation",
                "description": "Add description field for Phase I compatibility",
                "status": "active"
            }
        }
