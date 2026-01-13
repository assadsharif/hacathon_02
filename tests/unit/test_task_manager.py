"""Unit tests for task_manager functions (delete_task feature 003-delete-task).

Tests follow TDD RED-GREEN-REFACTOR cycle per constitution.
These tests should FAIL initially (RED phase) before implementation (GREEN phase).
"""
from datetime import datetime
import pytest
from src.task_manager import add_task, delete_task
from src.storage import _tasks


# ============================================================================
# User Story 1 (P1): Delete Task by ID - Core Functionality
# ============================================================================

def test_delete_task_removes_task_from_storage():
    """Test that delete_task removes the specified task from storage (US1).

    Validates FR-003: System MUST remove task from storage permanently.
    Validates SC-001: Users can delete any existing task by ID.
    Validates SC-002: Deleted tasks are permanently removed.
    """
    # Arrange: Create a task
    task = add_task("Task to delete", "This will be removed")
    task_id = task['id']

    # Act: Delete the task
    deleted = delete_task(task_id)

    # Assert: Task no longer in storage
    assert len(_tasks) == 0
    assert not any(t.id == task_id for t in _tasks)


def test_delete_task_returns_all_task_fields():
    """Test that delete_task returns dictionary with all task fields (US1).

    Validates FR-004: System MUST capture all task fields BEFORE deletion.
    Validates FR-005: System MUST return dictionary with all deleted task attributes.
    Validates SC-003: System returns complete task information before deletion.
    """
    # Arrange: Create a task with all fields populated
    task = add_task("Complete task", "With description")
    task_id = task['id']
    expected_title = "Complete task"
    expected_description = "With description"
    expected_completed = False

    # Act: Delete the task
    deleted = delete_task(task_id)

    # Assert: Return value contains all fields
    assert 'id' in deleted
    assert 'title' in deleted
    assert 'description' in deleted
    assert 'completed' in deleted
    assert 'created_at' in deleted

    assert deleted['id'] == task_id
    assert deleted['title'] == expected_title
    assert deleted['description'] == expected_description
    assert deleted['completed'] == expected_completed
    assert isinstance(deleted['created_at'], datetime)


def test_delete_task_only_removes_target_task():
    """Test that deleting one task does not affect other tasks (US1).

    Validates FR-009: Deletion of one task must not affect other tasks.
    Validates SC-004: Deletion of one task does not affect other tasks in storage.
    """
    # Arrange: Create multiple tasks
    task1 = add_task("Task 1", "First task")
    task2 = add_task("Task 2", "Second task")
    task3 = add_task("Task 3", "Third task")

    task1_id = task1['id']
    task2_id = task2['id']
    task3_id = task3['id']

    # Act: Delete the middle task
    delete_task(task2_id)

    # Assert: Tasks 1 and 3 still exist with unchanged data
    assert len(_tasks) == 2

    remaining_ids = [t.id for t in _tasks]
    assert task1_id in remaining_ids
    assert task2_id not in remaining_ids
    assert task3_id in remaining_ids

    # Verify task data unchanged
    task1_obj = next(t for t in _tasks if t.id == task1_id)
    assert task1_obj.title == "Task 1"
    assert task1_obj.description == "First task"

    task3_obj = next(t for t in _tasks if t.id == task3_id)
    assert task3_obj.title == "Task 3"
    assert task3_obj.description == "Third task"


def test_delete_task_prints_confirmation_message(capsys):
    """Test that delete_task prints confirmation message with task details (US1).

    Validates FR-006: System MUST display confirmation message after successful deletion.
    """
    # Arrange: Create a task
    task = add_task("Task to confirm", "Confirmation test")
    task_id = task['id']

    # Act: Delete the task
    delete_task(task_id)

    # Assert: Confirmation message printed
    captured = capsys.readouterr()
    assert f"✓ Task #{task_id} deleted: Task to confirm" in captured.out


# ============================================================================
# User Story 2 (P2): Handle Invalid Delete Attempts - Error Handling
# ============================================================================

def test_delete_task_raises_error_for_nonexistent_id():
    """Test that delete_task raises ValueError when task ID doesn't exist (US2).

    Validates FR-008: System MUST raise ValueError when task ID doesn't exist.
    Validates SC-005: System handles non-existent task IDs gracefully.
    """
    # Arrange: Create some tasks (but not ID 999)
    add_task("Task 1", "First")
    add_task("Task 2", "Second")

    # Act & Assert: Deleting non-existent ID raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(999)

    assert "Task #999 not found" in str(exc_info.value)


def test_delete_task_prints_error_for_nonexistent_id(capsys):
    """Test that delete_task prints error message when task not found (US2).

    Validates FR-007: System MUST display error message when task ID doesn't exist.
    """
    # Arrange: Create a task (ID will be 1)
    add_task("Task 1", "First")

    # Act: Try to delete non-existent task
    with pytest.raises(ValueError):
        delete_task(999)

    # Assert: Error message printed
    captured = capsys.readouterr()
    assert "✗ Error: Task #999 not found" in captured.out


def test_delete_task_leaves_storage_unchanged_on_error():
    """Test that delete_task doesn't modify storage when task not found (US2).

    Validates FR-009: Deletion must not affect other tasks.
    Validates SC-005: No state corruption on error.
    """
    # Arrange: Create tasks
    task1 = add_task("Task 1", "First")
    task2 = add_task("Task 2", "Second")

    initial_count = len(_tasks)

    # Act: Try to delete non-existent task
    with pytest.raises(ValueError):
        delete_task(999)

    # Assert: Storage unchanged
    assert len(_tasks) == initial_count
    assert any(t.id == task1['id'] for t in _tasks)
    assert any(t.id == task2['id'] for t in _tasks)


def test_delete_task_fails_on_double_deletion():
    """Test that deleting the same task twice raises error on second attempt (US2).

    Validates FR-010: System handles empty storage case.
    Validates SC-002: Deleted tasks permanently removed.
    """
    # Arrange: Create and delete a task
    task = add_task("Task to delete twice", "Double deletion test")
    task_id = task['id']
    delete_task(task_id)

    # Act & Assert: Second deletion raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(task_id)

    assert f"Task #{task_id} not found" in str(exc_info.value)


# ============================================================================
# Edge Cases - Additional Testing
# ============================================================================

def test_delete_task_works_with_single_task():
    """Test that deleting the only task leaves storage empty (Edge Case).

    Validates delete_task handles single-item list correctly.
    """
    # Arrange: Create a single task
    task = add_task("Only task", "Single task in storage")
    task_id = task['id']

    # Act: Delete the only task
    deleted = delete_task(task_id)

    # Assert: Storage is now empty
    assert len(_tasks) == 0
    assert deleted['id'] == task_id
    assert deleted['title'] == "Only task"


def test_delete_task_handles_first_task():
    """Test that deleting the first task (index 0) works correctly (Edge Case).

    Validates delete_task handles list head deletion without index errors.
    """
    # Arrange: Create multiple tasks
    task1 = add_task("First task", "Index 0")
    task2 = add_task("Second task", "Index 1")
    task3 = add_task("Third task", "Index 2")

    # Act: Delete the first task
    deleted = delete_task(task1['id'])

    # Assert: First task removed, others remain
    assert len(_tasks) == 2
    assert deleted['id'] == task1['id']
    assert deleted['title'] == "First task"

    remaining_ids = [t.id for t in _tasks]
    assert task1['id'] not in remaining_ids
    assert task2['id'] in remaining_ids
    assert task3['id'] in remaining_ids


def test_delete_task_handles_last_task():
    """Test that deleting the last task works correctly (Edge Case).

    Validates delete_task handles list tail deletion without index errors.
    """
    # Arrange: Create multiple tasks
    task1 = add_task("First task", "Index 0")
    task2 = add_task("Second task", "Index 1")
    task3 = add_task("Last task", "Index 2")

    # Act: Delete the last task
    deleted = delete_task(task3['id'])

    # Assert: Last task removed, others remain
    assert len(_tasks) == 2
    assert deleted['id'] == task3['id']
    assert deleted['title'] == "Last task"

    remaining_ids = [t.id for t in _tasks]
    assert task1['id'] in remaining_ids
    assert task2['id'] in remaining_ids
    assert task3['id'] not in remaining_ids


def test_delete_task_fails_on_empty_storage():
    """Test that delete_task raises ValueError when storage is empty (Edge Case).

    Validates delete_task handles empty list without runtime errors.
    """
    # Arrange: Ensure storage is empty (conftest.py auto-resets)
    assert len(_tasks) == 0

    # Act & Assert: Deleting from empty storage raises ValueError
    with pytest.raises(ValueError) as exc_info:
        delete_task(1)

    assert "Task #1 not found" in str(exc_info.value)

    # Assert: Storage still empty after failed deletion
    assert len(_tasks) == 0
