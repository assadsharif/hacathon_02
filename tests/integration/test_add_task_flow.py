"""Integration tests for complete add task flow (001-add-task).

Tests the end-to-end flow from user input through storage and confirmation.
Following TDD RED-GREEN-REFACTOR cycle per constitution.
"""
import pytest
from src.task_manager import add_task
from src.storage import _tasks


def test_add_basic_task_flow():
    """Test complete flow of adding a basic task (US1).

    Validates end-to-end integration:
    - Title validation
    - ID generation
    - Task creation
    - Storage
    - Return value format
    - Confirmation (tested via return value)
    """
    # Start with known state
    initial_count = len(_tasks)

    # Add task
    result = add_task("Buy groceries")

    # Verify return value structure (FR-007)
    assert isinstance(result, dict)
    assert 'id' in result
    assert 'title' in result
    assert 'description' in result
    assert 'completed' in result
    assert 'created_at' in result

    # Verify values
    assert result['id'] == initial_count + 1
    assert result['title'] == "Buy groceries"
    assert result['description'] is None
    assert result['completed'] is False

    # Verify stored in memory (FR-006)
    assert len(_tasks) == initial_count + 1
    stored_task = _tasks[-1]
    assert stored_task.id == result['id']
    assert stored_task.title == result['title']


def test_add_task_with_description_flow():
    """Test complete flow of adding a task with description (US2).

    Validates end-to-end integration with optional description:
    - Title and description acceptance
    - Storage of both fields
    - Return value includes description
    """
    initial_count = len(_tasks)

    # Add task with description
    result = add_task("Write report", "Q4 performance report")

    # Verify return value structure
    assert isinstance(result, dict)
    assert result['title'] == "Write report"
    assert result['description'] == "Q4 performance report"
    assert result['completed'] is False

    # Verify stored in memory with description
    assert len(_tasks) == initial_count + 1
    stored_task = _tasks[-1]
    assert stored_task.description == "Q4 performance report"
