"""
[Task]: AUTH-A1
[From]: authentication.spec.md FR-AUTH-001, plan.md Database Schema

User Model - SQLModel table definition for authentication

This model stores user authentication data for Better Auth integration.
Passwords are hashed, never stored in plain text.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
import uuid


class User(SQLModel, table=True):
    """
    User table model for authentication.

    This model stores user accounts for the authentication system.
    Works with Better Auth for password hashing and session management.

    Table: users

    Fields:
        id: UUID primary key (auto-generated)
        email: Unique email address (login identifier)
        password_hash: Hashed password (bcrypt/argon2)
        name: Optional display name
        created_at: Account creation timestamp
    """

    __tablename__ = "users"

    # Primary key (UUID)
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        description="Unique user identifier (UUID)"
    )

    # Email (unique, required)
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        description="User email address (unique, used for login)"
    )

    # Password hash (never store plain text)
    password_hash: str = Field(
        max_length=255,
        description="Hashed password (bcrypt/argon2)"
    )

    # Optional display name
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User display name (optional)"
    )

    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    def __repr__(self) -> str:
        """String representation of User"""
        return f"User(id={self.id}, email='{self.email}', name='{self.name}')"

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe"
            }
        }
