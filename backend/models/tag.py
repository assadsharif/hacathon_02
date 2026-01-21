"""
[Task]: T012
Tag and TodoTag Models - SQLModel table definitions for tagging system

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/data-model.md
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from datetime import datetime
from typing import Optional
import uuid


class Tag(SQLModel, table=True):
    """
    Tag table model for categorizing tasks.

    Each user has their own set of unique tags.

    Table: tags

    Fields:
        id: Primary key, auto-incremented
        name: Tag name (unique per user)
        user_id: Owner of the tag
        created_at: Timestamp when tag was created
    """

    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uq_tag_name_user"),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the tag"
    )

    name: str = Field(
        max_length=50,
        min_length=1,
        description="Tag name (1-50 characters)"
    )

    user_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PGUUID(as_uuid=True), ForeignKey("users.id"), index=True),
        description="User ID (owner of this tag)"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when tag was created"
    )

    def __repr__(self) -> str:
        """String representation of Tag"""
        return f"Tag(id={self.id}, name='{self.name}')"

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "name": "work",
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class TodoTag(SQLModel, table=True):
    """
    Junction table for many-to-many relationship between todos and tags.

    Table: todo_tags

    Fields:
        todo_id: Foreign key to todos table
        tag_id: Foreign key to tags table
    """

    __tablename__ = "todo_tags"

    todo_id: int = Field(
        foreign_key="todos.id",
        primary_key=True,
        description="Todo ID"
    )

    tag_id: int = Field(
        foreign_key="tags.id",
        primary_key=True,
        description="Tag ID"
    )

    def __repr__(self) -> str:
        """String representation of TodoTag"""
        return f"TodoTag(todo_id={self.todo_id}, tag_id={self.tag_id})"
