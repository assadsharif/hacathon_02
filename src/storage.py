"""In-memory task storage.

This module provides the TaskStore class for managing tasks in memory,
following the specification at /specs/phase1/features/add-task.md.
"""
from datetime import datetime
from typing import Any

from .models import Task


class TaskStore:
    """In-memory task storage manager.

    Manages a collection of tasks stored in memory with automatic ID assignment.
    All data is lost when the application terminates (no persistence).
    """

    def __init__(self) -> None:
        """Initialize the task store with empty storage."""
        self._tasks: list[Task] = []
        self._task_id_counter: int = 0

    def add_task(self, title: str, description: str | None = None) -> dict[str, Any]:
        """Add a new task to the in-memory task list.

        Implements the function signature and behavior from the specification.
        Validates input, assigns unique ID, creates task, and stores in memory.

        Args:
            title: The task title (required, non-empty)
            description: Optional task description

        Returns:
            Dictionary containing task details:
            {
                'id': int,
                'title': str,
                'description': str | None,
                'completed': bool,
                'created_at': datetime
            }

        Raises:
            ValueError: If title is empty or None

        Examples:
            >>> store = TaskStore()
            >>> task = store.add_task("Buy groceries")
            >>> print(task['id'])
            1
            >>> task = store.add_task("Write report", "Q4 performance")
            >>> print(task['description'])
            'Q4 performance'
        """
        # Validation Rule 1 & 2: Title must not be None and must not be empty
        if title is None:
            raise ValueError("Task title is required")

        if isinstance(title, str) and title.strip() == "":
            raise ValueError("Task title is required")

        # Increment ID counter (IDs start from 1)
        self._task_id_counter += 1

        # Create task with auto-assigned ID and current timestamp
        task = Task(
            id=self._task_id_counter,
            title=title.strip(),
            description=description,
            completed=False,
            created_at=datetime.now()
        )

        # Store in memory
        self._tasks.append(task)

        # Return task as dictionary
        return task.to_dict()

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks from in-memory storage.

        Returns:
            List of all Task objects (copy to prevent external modification)
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Retrieve a specific task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def clear_all_tasks(self) -> None:
        """Clear all tasks from in-memory storage.

        Resets the task list and ID counter.
        Useful for testing purposes.
        """
        self._tasks.clear()
        self._task_id_counter = 0

    def task_count(self) -> int:
        """Get the total number of tasks.

        Returns:
            Number of tasks in storage
        """
        return len(self._tasks)

    def delete_task(self, task_id: int) -> dict[str, Any]:
        """Delete a task from the in-memory task list.

        Implements the specification at /specs/phase1/features/delete-task.md.

        Args:
            task_id: The unique task identifier

        Returns:
            Dictionary containing deleted task details:
            {
                'id': int,
                'title': str,
                'description': str | None,
                'completed': bool,
                'created_at': datetime
            }

        Raises:
            ValueError: If task with specified ID does not exist

        Examples:
            >>> store = TaskStore()
            >>> store.add_task("Buy groceries")
            >>> deleted = store.delete_task(1)
            >>> print(deleted['title'])
            'Buy groceries'
        """
        # Find the task
        task = self.get_task_by_id(task_id)

        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Remove from list
        self._tasks.remove(task)

        # Return deleted task as dictionary
        return task.to_dict()

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None
    ) -> dict[str, Any]:
        """Update an existing task's details.

        Implements the specification at /specs/phase1/features/update-task.md.

        Args:
            task_id: The unique task identifier
            title: New task title (optional, must be non-empty if provided)
            description: New task description (optional, can be None to remove)

        Returns:
            Dictionary containing updated task details:
            {
                'id': int,
                'title': str,
                'description': str | None,
                'completed': bool,
                'created_at': datetime
            }

        Raises:
            ValueError: If task not found, no fields provided, or title is empty

        Examples:
            >>> store = TaskStore()
            >>> store.add_task("Buy groceries")
            >>> updated = store.update_task(1, title="Buy organic groceries")
            >>> print(updated['title'])
            'Buy organic groceries'
        """
        # Find the task
        task = self.get_task_by_id(task_id)

        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Check if at least one field is provided
        if title is None and description is None:
            raise ValueError("No fields to update")

        # Update title if provided
        if title is not None:
            if isinstance(title, str) and title.strip() == "":
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        # Update description if provided (even if None)
        if description is not None or 'description' in locals():
            # This allows explicitly setting description to None
            task.description = description

        # Return updated task as dictionary
        return task.to_dict()

    def toggle_task_completion(self, task_id: int) -> dict[str, Any]:
        """Toggle the completion status of a task.

        Implements the specification at /specs/phase1/features/mark-complete.md.

        Args:
            task_id: The unique task identifier

        Returns:
            Dictionary containing updated task details:
            {
                'id': int,
                'title': str,
                'description': str | None,
                'completed': bool,  # Toggled value
                'created_at': datetime
            }

        Raises:
            ValueError: If task with specified ID does not exist

        Examples:
            >>> store = TaskStore()
            >>> store.add_task("Buy groceries")
            >>> task = store.toggle_task_completion(1)
            >>> print(task['completed'])
            True
            >>> task = store.toggle_task_completion(1)
            >>> print(task['completed'])
            False
        """
        # Find the task
        task = self.get_task_by_id(task_id)

        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Toggle completion status
        task.completed = not task.completed

        # Return updated task as dictionary
        return task.to_dict()

    def search_tasks(
        self,
        keyword: str | None = None,
        status_filter: str = "all"
    ) -> list[Task]:
        """Search and filter tasks.

        Implements the specification at /specs/phase1/features/search-filter-tasks.md.

        Args:
            keyword: Search keyword (searches in title and description, case-insensitive)
            status_filter: Filter by status ("all", "completed", "incomplete")

        Returns:
            List of Task objects matching the criteria

        Examples:
            >>> store = TaskStore()
            >>> store.add_task("Buy groceries")
            >>> store.add_task("Call dentist")
            >>> results = store.search_tasks(keyword="buy")
            >>> len(results)
            1
        """
        results = self._tasks.copy()

        # Filter by keyword
        if keyword:
            keyword_lower = keyword.lower()
            results = [
                task for task in results
                if keyword_lower in task.title.lower() or
                (task.description and keyword_lower in task.description.lower())
            ]

        # Filter by status
        if status_filter == "completed":
            results = [task for task in results if task.completed]
        elif status_filter == "incomplete":
            results = [task for task in results if not task.completed]

        return results

    def get_sorted_tasks(self, sort_by: str = "id", reverse: bool = False) -> list[Task]:
        """Get tasks sorted by specified criteria.

        Implements the specification at /specs/phase1/features/sort-tasks.md.

        Args:
            sort_by: Sort criterion ("id", "title", "created", "status")
            reverse: Sort in reverse order (default: False)

        Returns:
            List of Task objects sorted by the specified criterion

        Examples:
            >>> store = TaskStore()
            >>> store.add_task("Task C")
            >>> store.add_task("Task A")
            >>> sorted_tasks = store.get_sorted_tasks(sort_by="title")
            >>> sorted_tasks[0].title
            'Task A'
        """
        tasks = self._tasks.copy()

        if sort_by == "id":
            tasks.sort(key=lambda t: t.id, reverse=reverse)
        elif sort_by == "title":
            tasks.sort(key=lambda t: t.title.lower(), reverse=reverse)
        elif sort_by == "created":
            tasks.sort(key=lambda t: t.created_at, reverse=reverse)
        elif sort_by == "status":
            # Sort by completion status (incomplete first, then completed)
            # Within each group, maintain ID order
            tasks.sort(key=lambda t: (t.completed, t.id), reverse=reverse)

        return tasks
