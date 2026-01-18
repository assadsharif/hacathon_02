"""Integration tests for toggle_task_completion feature (002-mark-complete).

Tests verify toggle_task_completion integrates correctly with add_task from 001-add-task.
Tests validate end-to-end workflows and multi-operation scenarios.
"""
from datetime import datetime
import pytest
from src.task_manager import add_task, toggle_task_completion
from src.storage import _tasks


# ============================================================================
# Integration Tests - toggle_task_completion with add_task
# ============================================================================


def test_complete_workflow_add_and_toggle():
    """Test complete workflow: add task then toggle completion (Integration).

    Validates integration between 001-add-task and 002-mark-complete features.
    Validates end-to-end user workflow.
    """
    # Arrange & Act: Add task (from 001-add-task)
    task = add_task("New task", "To be completed")
    task_id = task['id']

    # Verify task created with completed=False
    assert task['completed'] is False
    assert task['title'] == "New task"
    assert task['description'] == "To be completed"

    # Act: Toggle to complete (from 002-mark-complete)
    toggled = toggle_task_completion(task_id)

    # Assert: Task marked as complete
    assert toggled['id'] == task_id
    assert toggled['completed'] is True

    # Assert: All other fields preserved from add_task
    assert toggled['title'] == task['title']
    assert toggled['description'] == task['description']
    assert toggled['created_at'] == task['created_at']

    # Act: Toggle back to incomplete
    toggled_back = toggle_task_completion(task_id)

    # Assert: Task marked as incomplete
    assert toggled_back['completed'] is False
    assert toggled_back['title'] == task['title']


def test_toggle_multiple_tasks_independently():
    """Test toggling multiple tasks independently without interference (Integration).

    Validates that toggle operations on different tasks don't affect each other.
    Validates data isolation between tasks.
    """
    # Arrange: Add multiple tasks
    task1 = add_task("Task 1", "First task")
    task2 = add_task("Task 2", "Second task")
    task3 = add_task("Task 3", "Third task")

    # Verify all start incomplete
    assert task1['completed'] is False
    assert task2['completed'] is False
    assert task3['completed'] is False

    # Act: Toggle task1 and task3 to complete (leave task2 incomplete)
    toggle_task_completion(task1['id'])
    toggle_task_completion(task3['id'])

    # Assert: Correct tasks completed
    task1_in_storage = next((t for t in _tasks if t.id == task1['id']), None)
    task2_in_storage = next((t for t in _tasks if t.id == task2['id']), None)
    task3_in_storage = next((t for t in _tasks if t.id == task3['id']), None)

    assert task1_in_storage.completed is True
    assert task2_in_storage.completed is False  # Unchanged
    assert task3_in_storage.completed is True

    # Act: Toggle task1 back to incomplete
    toggle_task_completion(task1['id'])

    # Assert: Only task1 affected
    task1_in_storage = next((t for t in _tasks if t.id == task1['id']), None)
    task2_in_storage = next((t for t in _tasks if t.id == task2['id']), None)
    task3_in_storage = next((t for t in _tasks if t.id == task3['id']), None)

    assert task1_in_storage.completed is False
    assert task2_in_storage.completed is False  # Still unchanged
    assert task3_in_storage.completed is True  # Still complete

    # Verify all original field values preserved
    assert task1_in_storage.title == "Task 1"
    assert task2_in_storage.title == "Task 2"
    assert task3_in_storage.title == "Task 3"
