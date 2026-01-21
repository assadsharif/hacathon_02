"""
Todo API Routes

This module implements all RESTful CRUD endpoints for todo operations.
All endpoints mirror Phase I domain logic with database persistence.

[Task]: AUTH-B3 - Added JWT authentication and user-scoped data filtering
[Task]: T015, T017, T023-T026 - Phase V event-driven architecture

All endpoints now require authentication and filter todos by user_id.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List, Optional, Literal
from datetime import datetime
import uuid

from database import get_session
from models import Todo
from schemas import (
    TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, RecurrenceSchema
)
from auth import get_current_user_id
from services.todo_service import TodoService, get_todo_service
from services.tag_service import TagService

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/todos",
    tags=["Todos"],
    responses={
        404: {"description": "Todo not found"},
        422: {"description": "Validation error"}
    }
)


def _todo_to_response(todo: Todo, tags: List[str]) -> TodoResponse:
    """Convert Todo model to TodoResponse with tags."""
    recurrence = None
    if todo.recurrence_rule:
        recurrence = RecurrenceSchema(
            rule=todo.recurrence_rule,
            interval=todo.recurrence_interval,
            end_date=todo.recurrence_end_date
        )

    return TodoResponse(
        id=todo.id,
        user_id=todo.user_id,
        title=todo.title,
        description=todo.description,
        status=todo.status,
        priority=todo.priority,
        due_date=todo.due_date,
        reminder_at=todo.reminder_at,
        recurrence=recurrence,
        tags=tags,
        parent_task_id=todo.parent_task_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.get("/", response_model=TodoListResponse, status_code=status.HTTP_200_OK)
async def list_todos(
    user_id: uuid.UUID = Depends(get_current_user_id),
    status_filter: Optional[Literal["active", "completed", "all"]] = Query(
        default="all", alias="status", description="Filter by status"
    ),
    priority: Optional[Literal["low", "medium", "high"]] = Query(
        default=None, description="Filter by priority"
    ),
    tag: Optional[str] = Query(
        default=None, description="Filter by tag name"
    ),
    due_before: Optional[datetime] = Query(
        default=None, description="Filter tasks due before this date"
    ),
    due_after: Optional[datetime] = Query(
        default=None, description="Filter tasks due after this date"
    ),
    search: Optional[str] = Query(
        default=None, description="Search in title and description"
    ),
    sort: Literal["created_at", "due_date", "priority", "title"] = Query(
        default="created_at", description="Sort field"
    ),
    order: Literal["asc", "desc"] = Query(
        default="desc", description="Sort order"
    ),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=20, ge=1, le=100, description="Items per page"),
    session: Session = Depends(get_session)
):
    """
    List all todos for authenticated user with filtering, sorting, and pagination.

    [Task]: T017 - Added filtering, sorting, search parameters

    Args:
        user_id: Authenticated user ID (extracted from JWT)
        status_filter: Filter by status (active, completed, all)
        priority: Filter by priority (low, medium, high)
        tag: Filter by tag name
        due_before: Filter tasks due before this date
        due_after: Filter tasks due after this date
        search: Search in title and description
        sort: Sort field (created_at, due_date, priority, title)
        order: Sort order (asc, desc)
        page: Page number (1-indexed)
        limit: Items per page (max 100)
        session: Database session (injected)

    Returns:
        TodoListResponse: Paginated list of user's todos

    Example:
        GET /api/todos
        GET /api/todos?status=active&priority=high
        GET /api/todos?tag=work&sort=due_date&order=asc
        GET /api/todos?search=meeting&page=2&limit=10
    """
    todo_service = get_todo_service(session)

    todos, total = todo_service.list_todos(
        user_id=user_id,
        status=status_filter,
        priority=priority,
        tag=tag,
        due_before=due_before,
        due_after=due_after,
        search=search,
        sort=sort,
        order=order,
        page=page,
        limit=limit
    )

    # Convert to response with tags
    items = []
    for todo in todos:
        tags = todo_service.get_tags_for_todo(todo.id, user_id)
        items.append(_todo_to_response(todo, tags))

    # Calculate total pages
    pages = (total + limit - 1) // limit if total > 0 else 1

    return TodoListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo(
    todo_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a single todo by ID for authenticated user.

    Args:
        todo_id: Todo ID
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Todo details with tags

    Raises:
        HTTPException 404: If todo not found or not owned by user
    """
    todo_service = get_todo_service(session)
    todo = todo_service.get_todo(todo_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    tags = todo_service.get_tags_for_todo(todo_id, user_id)
    return _todo_to_response(todo, tags)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for authenticated user.

    [Task]: T015 - Tag association on create
    [Task]: T023 - Publish task.created event

    Args:
        todo_data: Todo creation data
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Created todo with tags

    Example:
        POST /api/todos
        {
            "title": "Complete Phase V implementation",
            "description": "Add event-driven architecture",
            "priority": "high",
            "due_date": "2026-01-25T12:00:00Z",
            "tags": ["work", "important"]
        }
    """
    todo_service = get_todo_service(session)

    # Extract recurrence fields
    recurrence_rule = None
    recurrence_interval = 1
    recurrence_end_date = None
    if todo_data.recurrence:
        recurrence_rule = todo_data.recurrence.rule
        recurrence_interval = todo_data.recurrence.interval
        recurrence_end_date = todo_data.recurrence.end_date

    todo = await todo_service.create_todo(
        user_id=user_id,
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
        due_date=todo_data.due_date,
        reminder_at=todo_data.reminder_at,
        recurrence_rule=recurrence_rule,
        recurrence_interval=recurrence_interval,
        recurrence_end_date=recurrence_end_date,
        tags=todo_data.tags
    )

    tags = todo_service.get_tags_for_todo(todo.id, user_id)
    return _todo_to_response(todo, tags)


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing todo for authenticated user.

    [Task]: T015 - Tag association on update
    [Task]: T024, T025 - Publish task.updated/task.completed events

    Args:
        todo_id: Todo ID
        todo_data: Todo update data
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Updated todo

    Raises:
        HTTPException 404: If todo not found or not owned by user
    """
    todo_service = get_todo_service(session)

    # Extract recurrence fields if provided
    recurrence_rule = None
    recurrence_interval = None
    recurrence_end_date = None
    if todo_data.recurrence is not None:
        recurrence_rule = todo_data.recurrence.rule
        recurrence_interval = todo_data.recurrence.interval
        recurrence_end_date = todo_data.recurrence.end_date

    todo = await todo_service.update_todo(
        todo_id=todo_id,
        user_id=user_id,
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status,
        priority=todo_data.priority,
        due_date=todo_data.due_date,
        reminder_at=todo_data.reminder_at,
        recurrence_rule=recurrence_rule,
        recurrence_interval=recurrence_interval,
        recurrence_end_date=recurrence_end_date,
        tags=todo_data.tags
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    tags = todo_service.get_tags_for_todo(todo_id, user_id)
    return _todo_to_response(todo, tags)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a todo for authenticated user.

    [Task]: T026 - Publish task.deleted event

    Args:
        todo_id: Todo ID
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 404: If todo not found or not owned by user
    """
    todo_service = get_todo_service(session)
    deleted = await todo_service.delete_todo(todo_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    return None


@router.post("/{todo_id}/complete", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def complete_todo(
    todo_id: int,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Mark a todo as completed.

    [Task]: T025 - Publish task.completed event

    Args:
        todo_id: Todo ID
        user_id: Authenticated user ID (extracted from JWT)
        session: Database session (injected)

    Returns:
        TodoResponse: Completed todo

    Raises:
        HTTPException 404: If todo not found or not owned by user
    """
    todo_service = get_todo_service(session)
    todo = await todo_service.complete_todo(todo_id, user_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

    tags = todo_service.get_tags_for_todo(todo_id, user_id)
    return _todo_to_response(todo, tags)
