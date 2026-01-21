"""
[Task]: T015, T023-T026
Todo Service - Business logic for todo operations with tag association and event publishing

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/data-model.md
"""

from sqlmodel import Session, select, or_, and_, func
from sqlalchemy import desc, asc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import uuid
import logging

from models.todo import Todo
from models.tag import Tag, TodoTag
from services.tag_service import TagService
from services.event_publisher import get_event_publisher, EventPublisher

logger = logging.getLogger(__name__)


class TodoService:
    """
    Service for managing todos with tag association and event publishing.

    [Task]: T015 - Tag association logic
    [Task]: T023-T026 - Event publishing integration
    """

    def __init__(self, session: Session):
        self.session = session
        self.tag_service = TagService(session)
        self.event_publisher: EventPublisher = get_event_publisher()

    async def create_todo(
        self,
        user_id: uuid.UUID,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        due_date: Optional[datetime] = None,
        reminder_at: Optional[datetime] = None,
        recurrence_rule: Optional[str] = None,
        recurrence_interval: int = 1,
        recurrence_end_date: Optional[datetime] = None,
        tags: List[str] = None
    ) -> Todo:
        """
        Create a new todo with optional tags.

        [Task]: T015 - Tag association on create
        [Task]: T023 - Publish task.created event

        Args:
            user_id: Owner's user ID
            title: Todo title
            description: Optional description
            priority: Task priority (low, medium, high)
            due_date: Optional due date
            reminder_at: Optional reminder time
            recurrence_rule: Optional recurrence pattern
            recurrence_interval: Recurrence interval
            recurrence_end_date: Optional recurrence end date
            tags: List of tag names to associate

        Returns:
            Created Todo object with tags
        """
        tags = tags or []

        # Create todo
        todo = Todo(
            user_id=user_id,
            title=title,
            description=description,
            status="active",
            priority=priority,
            due_date=due_date,
            reminder_at=reminder_at,
            recurrence_rule=recurrence_rule,
            recurrence_interval=recurrence_interval,
            recurrence_end_date=recurrence_end_date
        )

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        # [Task]: T015 - Associate tags
        if tags:
            self.tag_service.set_tags_for_todo(todo.id, tags, user_id)

        # [Task]: T023 - Publish task.created event
        try:
            await self.event_publisher.publish_task_created(
                task_id=todo.id,
                user_id=user_id,
                title=title,
                description=description,
                status="active",
                priority=priority,
                due_date=due_date,
                reminder_at=reminder_at,
                recurrence_rule=recurrence_rule,
                recurrence_interval=recurrence_interval,
                recurrence_end_date=recurrence_end_date,
                tags=tags,
                created_at=todo.created_at
            )
        except Exception as e:
            logger.error(f"Failed to publish task.created event: {e}")

        return todo

    async def update_todo(
        self,
        todo_id: int,
        user_id: uuid.UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None,
        reminder_at: Optional[datetime] = None,
        recurrence_rule: Optional[str] = None,
        recurrence_interval: Optional[int] = None,
        recurrence_end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Todo]:
        """
        Update an existing todo.

        [Task]: T015 - Tag association on update
        [Task]: T024 - Publish task.updated event
        [Task]: T025 - Publish task.completed event on status change

        Args:
            todo_id: Todo ID
            user_id: Owner's user ID
            **kwargs: Fields to update

        Returns:
            Updated Todo object or None if not found
        """
        # Get existing todo
        query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = self.session.exec(query).first()

        if not todo:
            return None

        # Track changes for event
        changes: Dict[str, Dict[str, Any]] = {}
        old_status = todo.status

        # Update fields
        update_fields = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "reminder_at": reminder_at,
            "recurrence_rule": recurrence_rule,
            "recurrence_interval": recurrence_interval,
            "recurrence_end_date": recurrence_end_date
        }

        for field, value in update_fields.items():
            if value is not None:
                old_value = getattr(todo, field)
                if old_value != value:
                    changes[field] = {"old": str(old_value) if old_value else None, "new": str(value)}
                    setattr(todo, field, value)

        # Update timestamp
        todo.updated_at = datetime.utcnow()

        # [Task]: T015 - Update tags if provided
        if tags is not None:
            old_tags = [t.name for t in self.tag_service.get_tags_for_todo(todo_id, user_id)]
            if set(old_tags) != set(tags):
                changes["tags"] = {"old": old_tags, "new": tags}
                self.tag_service.set_tags_for_todo(todo_id, tags, user_id)

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        # [Task]: T025 - Publish task.completed event if status changed to completed
        if status == "completed" and old_status != "completed":
            try:
                await self.event_publisher.publish_task_completed(
                    task_id=todo.id,
                    user_id=user_id,
                    is_recurring=todo.is_recurring,
                    recurrence_rule=todo.recurrence_rule,
                    recurrence_interval=todo.recurrence_interval,
                    completed_at=todo.updated_at
                )
            except Exception as e:
                logger.error(f"Failed to publish task.completed event: {e}")
        # [Task]: T024 - Publish task.updated event for other changes
        elif changes:
            try:
                await self.event_publisher.publish_task_updated(
                    task_id=todo.id,
                    user_id=user_id,
                    changes=changes,
                    updated_at=todo.updated_at
                )
            except Exception as e:
                logger.error(f"Failed to publish task.updated event: {e}")

        return todo

    async def delete_todo(self, todo_id: int, user_id: uuid.UUID) -> bool:
        """
        Delete a todo.

        [Task]: T026 - Publish task.deleted event

        Args:
            todo_id: Todo ID
            user_id: Owner's user ID

        Returns:
            True if deleted, False if not found
        """
        query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = self.session.exec(query).first()

        if not todo:
            return False

        # Remove tag associations first
        tag_query = select(TodoTag).where(TodoTag.todo_id == todo_id)
        for todo_tag in self.session.exec(tag_query).all():
            self.session.delete(todo_tag)

        # Delete todo
        self.session.delete(todo)
        self.session.commit()

        # [Task]: T026 - Publish task.deleted event
        try:
            await self.event_publisher.publish_task_deleted(
                task_id=todo_id,
                user_id=user_id,
                deleted_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to publish task.deleted event: {e}")

        return True

    def get_todo(self, todo_id: int, user_id: uuid.UUID) -> Optional[Todo]:
        """Get a single todo by ID."""
        query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return self.session.exec(query).first()

    def list_todos(
        self,
        user_id: uuid.UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        search: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc",
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Todo], int]:
        """
        List todos with filtering, sorting, and pagination.

        [Task]: T017 - Filtering, sorting, search parameters

        Args:
            user_id: Owner's user ID
            status: Filter by status (active, completed, all)
            priority: Filter by priority
            tag: Filter by tag name
            due_before: Filter tasks due before this date
            due_after: Filter tasks due after this date
            search: Search in title and description
            sort: Sort field (created_at, due_date, priority, title)
            order: Sort order (asc, desc)
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (todos list, total count)
        """
        # Base query
        query = select(Todo).where(Todo.user_id == user_id)
        count_query = select(func.count()).select_from(Todo).where(Todo.user_id == user_id)

        # Status filter
        if status and status != "all":
            query = query.where(Todo.status == status)
            count_query = count_query.where(Todo.status == status)

        # Priority filter
        if priority:
            query = query.where(Todo.priority == priority)
            count_query = count_query.where(Todo.priority == priority)

        # Due date filters
        if due_before:
            query = query.where(Todo.due_date <= due_before)
            count_query = count_query.where(Todo.due_date <= due_before)

        if due_after:
            query = query.where(Todo.due_date >= due_after)
            count_query = count_query.where(Todo.due_date >= due_after)

        # Search filter
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Todo.title.ilike(search_pattern),
                    Todo.description.ilike(search_pattern)
                )
            )
            count_query = count_query.where(
                or_(
                    Todo.title.ilike(search_pattern),
                    Todo.description.ilike(search_pattern)
                )
            )

        # Tag filter - join with TodoTag and Tag tables
        if tag:
            tag_obj = self.session.exec(
                select(Tag).where(Tag.name == tag.lower().strip(), Tag.user_id == user_id)
            ).first()
            if tag_obj:
                query = query.join(TodoTag, Todo.id == TodoTag.todo_id).where(
                    TodoTag.tag_id == tag_obj.id
                )
                count_query = count_query.join(TodoTag, Todo.id == TodoTag.todo_id).where(
                    TodoTag.tag_id == tag_obj.id
                )
            else:
                # Tag not found, return empty result
                return [], 0

        # Get total count
        total = self.session.exec(count_query).one()

        # Sorting
        sort_column = getattr(Todo, sort, Todo.created_at)
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        todos = list(self.session.exec(query).all())

        return todos, total

    def get_tags_for_todo(self, todo_id: int, user_id: uuid.UUID) -> List[str]:
        """Get tag names for a todo."""
        tags = self.tag_service.get_tags_for_todo(todo_id, user_id)
        return [tag.name for tag in tags]

    async def complete_todo(self, todo_id: int, user_id: uuid.UUID) -> Optional[Todo]:
        """
        Mark a todo as completed.

        [Task]: T025 - Publish task.completed event

        Args:
            todo_id: Todo ID
            user_id: Owner's user ID

        Returns:
            Updated Todo or None if not found
        """
        return await self.update_todo(todo_id, user_id, status="completed")


def get_todo_service(session: Session) -> TodoService:
    """Factory function to create TodoService instance."""
    return TodoService(session)
