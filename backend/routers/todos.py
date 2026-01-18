"""
Todo API Routes

This module implements all RESTful CRUD endpoints for todo operations.
All endpoints mirror Phase I domain logic with database persistence.

[Task]: AUTH-B3 - Added JWT authentication and user-scoped data filtering
All endpoints now require authentication and filter todos by user_id.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional, Literal
from datetime import datetime
import uuid

from database import get_session
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse
from auth import get_current_user_id  # [Task]: AUTH-B3

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/todos",
    tags=["Todos"],
    responses={
        404: {"description": "Todo not found"},
        422: {"description": "Validation error"}
    }
)


@router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def list_todos(
    user_id: uuid.UUID = Depends(get_current_user_id),  # [Task]: AUTH-B3
    status_filter: Optional[Literal["active", "completed"]] = None,
    session: Session = Depends(get_session)
):
    """
    List all todos for authenticated user with optional status filter.

    [Task]: AUTH-B3 - Added authentication and user-scoped filtering

    Args:
        user_id: Authenticated user ID (extracted from JWT)
        status_filter: Optional filter by status ("active" or "completed")
        session: Database session (injected)

    Returns:
        List[TodoResponse]: List of user's todos

    Raises:
        HTTPException 401: If JWT is invalid or missing

    Example:
        GET /api/todos
        GET /api/todos?status_filter=active
        GET /api/todos?status_filter=completed

    Security:
        Requires valid JWT token in Authorization header.
        Returns only todos owned by the authenticated user.
    """
    # Build query with user_id filter
    # [Task]: AUTH-B3 - Filter by authenticated user
    query = select(Todo).where(Todo.user_id == user_id)

    # Apply status filter if provided
    if status_filter:
        query = query.where(Todo.status == status_filter)

    # Execute query
    todos = session.exec(query).all()

    return todos


@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo(
    todo_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),  # [Task]: AUTH-B3
    session: Session = Depends(get_session)
):
    """
    Get a single todo by ID for authenticated user.

    [Task]: AUTH-B3 - Added authentication and user-scoped filtering

    Args:
        todo_id: Todo ID
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Todo details

    Raises:
        HTTPException 401: If JWT is invalid or missing
        HTTPException 404: If todo not found or not owned by user

    Example:
        GET /api/todos/1

    Security:
        Requires valid JWT token in Authorization header.
        Returns 404 if todo exists but is owned by another user (security: don't leak existence).
    """
    # Filter by both id and user_id for user-scoped access
    # [Task]: AUTH-B3 - Ensure user can only access their own todos
    query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(query).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),  # [Task]: AUTH-B3
    session: Session = Depends(get_session)
):
    """
    Create a new todo for authenticated user.

    [Task]: AUTH-B3 - Added authentication and automatic user_id assignment

    Args:
        todo_data: Todo creation data (title, description, status)
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Created todo with id and timestamps

    Raises:
        HTTPException 401: If JWT is invalid or missing

    Example:
        POST /api/todos
        {
            "title": "Complete Phase II implementation",
            "description": "Add description field for Phase I compatibility",
            "status": "active"
        }

    Security:
        Requires valid JWT token in Authorization header.
        Automatically assigns todo to authenticated user.
    """
    # Create todo instance from request data and set user_id
    # [Task]: AUTH-B3 - Assign todo to authenticated user
    todo = Todo(**todo_data.model_dump(), user_id=user_id)

    # Add to database
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),  # [Task]: AUTH-B3
    session: Session = Depends(get_session)
):
    """
    Update an existing todo for authenticated user.

    Only provided fields will be updated (partial update supported).

    [Task]: AUTH-B3 - Added authentication and user-scoped filtering

    Args:
        todo_id: Todo ID
        todo_data: Todo update data (title, description, and/or status)
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Updated todo

    Raises:
        HTTPException 401: If JWT is invalid or missing
        HTTPException 404: If todo not found or not owned by user

    Example:
        PUT /api/todos/1
        {
            "title": "Updated title",
            "description": "Updated description",
            "status": "completed"
        }

    Security:
        Requires valid JWT token in Authorization header.
        Returns 404 if todo exists but is owned by another user (security: don't leak existence).
    """
    # Get existing todo with user_id filter
    # [Task]: AUTH-B3 - Ensure user can only update their own todos
    query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(query).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    # Update only provided fields
    update_data = todo_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    # Update timestamp
    todo.updated_at = datetime.utcnow()

    # Save to database
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),  # [Task]: AUTH-B3
    session: Session = Depends(get_session)
):
    """
    Delete a todo for authenticated user.

    [Task]: AUTH-B3 - Added authentication and user-scoped filtering

    Args:
        todo_id: Todo ID
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 401: If JWT is invalid or missing
        HTTPException 404: If todo not found or not owned by user

    Example:
        DELETE /api/todos/1

    Security:
        Requires valid JWT token in Authorization header.
        Returns 404 if todo exists but is owned by another user (security: don't leak existence).
    """
    # Get existing todo with user_id filter
    # [Task]: AUTH-B3 - Ensure user can only delete their own todos
    query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(query).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    # Delete from database
    session.delete(todo)
    session.commit()

    # Return 204 No Content (no response body)
    return None
