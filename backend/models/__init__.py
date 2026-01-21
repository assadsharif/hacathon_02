"""
[Task]: AUTH-A1
[Task]: T012-T013 - Added Phase V models
[From]: authentication.spec.md, plan.md

SQLModel Database Models Package

This package contains all database table models using SQLModel.
Models are organized by domain for better maintainability.

Exports:
    - Todo: Todo table model (Phase I + Phase II + Phase V)
    - User: User table model (authentication)
    - Tag: Tag table model (Phase V)
    - TodoTag: Junction table for todo-tag relationship (Phase V)
"""

from models.todo import Todo
from models.user import User
from models.tag import Tag, TodoTag

__all__ = ["Todo", "User", "Tag", "TodoTag"]
