"""
[Task]: T014
Tag Service - CRUD operations for tags

Phase V: Event-Driven Architecture
Reference: specs/005-phase-v-event-driven/data-model.md
"""

from sqlmodel import Session, select
from typing import List, Optional
import uuid

from models.tag import Tag, TodoTag
from models.todo import Todo


class TagService:
    """Service for managing tags and tag associations."""

    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, name: str, user_id: uuid.UUID) -> Tag:
        """
        Create a new tag for a user.

        Args:
            name: Tag name (must be unique per user)
            user_id: Owner's user ID

        Returns:
            Created Tag object

        Raises:
            ValueError: If tag with same name already exists for user
        """
        # Check for existing tag
        existing = self.get_tag_by_name(name, user_id)
        if existing:
            raise ValueError(f"Tag '{name}' already exists for this user")

        tag = Tag(name=name.lower().strip(), user_id=user_id)
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def get_tag_by_id(self, tag_id: int, user_id: uuid.UUID) -> Optional[Tag]:
        """
        Get a tag by ID for a specific user.

        Args:
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            Tag object or None if not found
        """
        statement = select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        return self.session.exec(statement).first()

    def get_tag_by_name(self, name: str, user_id: uuid.UUID) -> Optional[Tag]:
        """
        Get a tag by name for a specific user.

        Args:
            name: Tag name
            user_id: Owner's user ID

        Returns:
            Tag object or None if not found
        """
        statement = select(Tag).where(
            Tag.name == name.lower().strip(),
            Tag.user_id == user_id
        )
        return self.session.exec(statement).first()

    def list_tags(self, user_id: uuid.UUID) -> List[Tag]:
        """
        List all tags for a user.

        Args:
            user_id: Owner's user ID

        Returns:
            List of Tag objects
        """
        statement = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        return list(self.session.exec(statement).all())

    def delete_tag(self, tag_id: int, user_id: uuid.UUID) -> bool:
        """
        Delete a tag by ID.

        Args:
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            True if deleted, False if not found
        """
        tag = self.get_tag_by_id(tag_id, user_id)
        if not tag:
            return False

        # Delete associations first (cascade should handle this, but be explicit)
        statement = select(TodoTag).where(TodoTag.tag_id == tag_id)
        for todo_tag in self.session.exec(statement).all():
            self.session.delete(todo_tag)

        self.session.delete(tag)
        self.session.commit()
        return True

    def add_tag_to_todo(self, todo_id: int, tag_id: int, user_id: uuid.UUID) -> bool:
        """
        Add a tag to a todo.

        Args:
            todo_id: Todo ID
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            True if added, False if already associated or invalid
        """
        # Verify ownership
        tag = self.get_tag_by_id(tag_id, user_id)
        if not tag:
            return False

        todo = self.session.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            return False

        # Check if already associated
        statement = select(TodoTag).where(
            TodoTag.todo_id == todo_id,
            TodoTag.tag_id == tag_id
        )
        if self.session.exec(statement).first():
            return True  # Already associated

        # Create association
        todo_tag = TodoTag(todo_id=todo_id, tag_id=tag_id)
        self.session.add(todo_tag)
        self.session.commit()
        return True

    def remove_tag_from_todo(self, todo_id: int, tag_id: int, user_id: uuid.UUID) -> bool:
        """
        Remove a tag from a todo.

        Args:
            todo_id: Todo ID
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            True if removed, False if not associated
        """
        # Verify ownership
        tag = self.get_tag_by_id(tag_id, user_id)
        if not tag:
            return False

        statement = select(TodoTag).where(
            TodoTag.todo_id == todo_id,
            TodoTag.tag_id == tag_id
        )
        todo_tag = self.session.exec(statement).first()
        if not todo_tag:
            return False

        self.session.delete(todo_tag)
        self.session.commit()
        return True

    def get_tags_for_todo(self, todo_id: int, user_id: uuid.UUID) -> List[Tag]:
        """
        Get all tags for a todo.

        Args:
            todo_id: Todo ID
            user_id: Owner's user ID

        Returns:
            List of Tag objects
        """
        statement = (
            select(Tag)
            .join(TodoTag, Tag.id == TodoTag.tag_id)
            .where(TodoTag.todo_id == todo_id, Tag.user_id == user_id)
            .order_by(Tag.name)
        )
        return list(self.session.exec(statement).all())

    def get_todos_by_tag(self, tag_id: int, user_id: uuid.UUID) -> List[Todo]:
        """
        Get all todos with a specific tag.

        Args:
            tag_id: Tag ID
            user_id: Owner's user ID

        Returns:
            List of Todo objects
        """
        statement = (
            select(Todo)
            .join(TodoTag, Todo.id == TodoTag.todo_id)
            .where(TodoTag.tag_id == tag_id, Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        return list(self.session.exec(statement).all())

    def set_tags_for_todo(
        self,
        todo_id: int,
        tag_names: List[str],
        user_id: uuid.UUID
    ) -> List[Tag]:
        """
        Set tags for a todo (replaces existing tags).

        Args:
            todo_id: Todo ID
            tag_names: List of tag names to set
            user_id: Owner's user ID

        Returns:
            List of Tag objects that were set
        """
        # Verify todo ownership
        todo = self.session.get(Todo, todo_id)
        if not todo or todo.user_id != user_id:
            raise ValueError("Todo not found or access denied")

        # Remove existing associations
        statement = select(TodoTag).where(TodoTag.todo_id == todo_id)
        for todo_tag in self.session.exec(statement).all():
            self.session.delete(todo_tag)

        # Add new tags (create if needed)
        tags = []
        for name in tag_names[:10]:  # Max 10 tags
            tag = self.get_tag_by_name(name, user_id)
            if not tag:
                tag = self.create_tag(name, user_id)
            tags.append(tag)

            todo_tag = TodoTag(todo_id=todo_id, tag_id=tag.id)
            self.session.add(todo_tag)

        self.session.commit()
        return tags


def get_tag_service(session: Session) -> TagService:
    """Factory function to create TagService instance."""
    return TagService(session)
