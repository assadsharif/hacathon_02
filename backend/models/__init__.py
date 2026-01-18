"""
[Task]: AUTH-A1
[From]: authentication.spec.md, plan.md

SQLModel Database Models Package

This package contains all database table models using SQLModel.
Models are organized by domain for better maintainability.

Exports:
    - Todo: Todo table model (Phase I + Phase II)
    - User: User table model (authentication)
"""

from models.todo import Todo
from models.user import User

__all__ = ["Todo", "User"]
