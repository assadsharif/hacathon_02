"""Unit tests for toggle_task_completion function (002-mark-complete feature).

Tests verify toggle functionality following TDD RED-GREEN-REFACTOR cycle.
Tests are organized by user story: US1 (core toggle) and US2 (error handling).
"""
from datetime import datetime
import pytest
from src.task_manager import add_task, toggle_task_completion
from src.storage import _tasks


# ============================================================================
# User Story 1 - Toggle Task Completion (Priority: P1)
# ============================================================================

def test_toggle_task_from_incomplete_to_complete():
    """Test that toggle_task_completion changes task from incomplete to complete (US1).

    Validates FR-003: System MUST toggle the completed field from False to True.
    Validates SC-001: Users can toggle completion status in single function call.
    """
    # Arrange: Create task (starts with completed=False)
    task = add_task("Task to complete", "Description")
    task_id = task['id']

    # Verify initial state
    assert task['completed'] is False

    # Act: Toggle from False to True
    updated = toggle_task_completion(task_id)

    # Assert: Task is now completed
    assert updated['id'] == task_id
    assert updated['completed'] is True
    assert updated['title'] == "Task to complete"
    assert updated['description'] == "Description"


def test_toggle_task_from_complete_to_incomplete():
    """Test that toggle_task_completion changes task from complete to incomplete (US1).

    Validates FR-003: System MUST toggle the completed field from True to False.
    Validates SC-002: System correctly toggles bidirectionally (False→True and True→False).
    """
    # Arrange: Create task and toggle to complete
    task = add_task("Already completed task", "Done")
    task_id = task['id']
    toggle_task_completion(task_id)  # Make it complete first

    # Verify task is completed
    assert any(t.id == task_id and t.completed is True for t in _tasks)

    # Act: Toggle from True to False
    updated = toggle_task_completion(task_id)

    # Assert: Task is now incomplete
    assert updated['id'] == task_id
    assert updated['completed'] is False
    assert updated['title'] == "Already completed task"


def test_toggle_multiple_times_returns_to_original_state():
    """Test that toggling multiple times alternates state correctly (US1).

    Validates SC-002: Bidirectional toggle works consistently.
    Validates that toggle operations are repeatable and predictable.
    """
    # Arrange: Create task (starts False)
    task = add_task("Toggle test", "Multiple toggles")
    task_id = task['id']

    initial_completed = task['completed']
    assert initial_completed is False

    # Act & Assert: Toggle twice should return to original state
    first_toggle = toggle_task_completion(task_id)
    assert first_toggle['completed'] is True  # False → True

    second_toggle = toggle_task_completion(task_id)
    assert second_toggle['completed'] is False  # True → False

    third_toggle = toggle_task_completion(task_id)
    assert third_toggle['completed'] is True  # False → True again

    # Verify final state in storage
    task_in_storage = next((t for t in _tasks if t.id == task_id), None)
    assert task_in_storage is not None
    assert task_in_storage.completed is True


def test_toggle_preserves_all_non_completion_fields():
    """Test that toggle_task_completion preserves all non-completion fields (US1).

    Validates FR-007: System MUST preserve all non-completed task fields.
    Validates SC-004: All non-completion task fields remain unchanged.
    """
    # Arrange: Create task with specific values
    task = add_task("Important task", "Detailed description")
    task_id = task['id']
    original_title = task['title']
    original_description = task['description']
    original_created_at = task['created_at']

    # Act: Toggle completion
    updated = toggle_task_completion(task_id)

    # Assert: All non-completion fields unchanged
    assert updated['id'] == task_id
    assert updated['title'] == original_title
    assert updated['description'] == original_description
    assert updated['created_at'] == original_created_at

    # Assert: Only completed field changed
    assert updated['completed'] is True  # Changed from False

    # Verify in storage
    task_in_storage = next((t for t in _tasks if t.id == task_id), None)
    assert task_in_storage.title == original_title
    assert task_in_storage.description == original_description
    assert task_in_storage.created_at == original_created_at


# ============================================================================
# Output Validation - User Story 1
# ============================================================================

def test_toggle_to_complete_displays_correct_message(capsys):
    """Test that toggling to complete displays correct confirmation message (US1).

    Validates FR-004: System MUST display "✓ Task #{id} marked as complete".
    Validates SC-003: Appropriate confirmation message displayed.
    """
    # Arrange: Create incomplete task
    task = add_task("Task to mark complete", "Description")
    task_id = task['id']
    capsys.readouterr()  # Clear output from add_task

    # Act: Toggle from False to True
    toggle_task_completion(task_id)

    # Assert: Correct message displayed
    captured = capsys.readouterr()
    assert f"✓ Task #{task_id} marked as complete" in captured.out


def test_toggle_to_incomplete_displays_correct_message(capsys):
    """Test that toggling to incomplete displays correct confirmation message (US1).

    Validates FR-005: System MUST display "✓ Task #{id} marked as incomplete".
    Validates SC-003: Appropriate confirmation message based on new status.
    """
    # Arrange: Create task and toggle to complete
    task = add_task("Task to mark incomplete", "Description")
    task_id = task['id']
    toggle_task_completion(task_id)  # Make it complete
    capsys.readouterr()  # Clear previous output

    # Act: Toggle from True to False
    toggle_task_completion(task_id)

    # Assert: Correct message displayed
    captured = capsys.readouterr()
    assert f"✓ Task #{task_id} marked as incomplete" in captured.out


# ============================================================================
# User Story 2 - Handle Invalid Task IDs (Priority: P2)
# ============================================================================

def test_toggle_non_existent_task_raises_error():
    """Test that toggle_task_completion raises ValueError for non-existent ID (US2).

    Validates FR-009: System MUST raise ValueError when task ID doesn't exist.
    Validates SC-005: Graceful error handling for invalid IDs.
    """
    # Arrange: Create some tasks
    add_task("Task 1", "First")
    add_task("Task 2", "Second")

    # Act & Assert: Toggling non-existent ID raises ValueError
    with pytest.raises(ValueError) as exc_info:
        toggle_task_completion(999)

    assert "Task #999 not found" in str(exc_info.value)


def test_toggle_non_existent_task_displays_error_message(capsys):
    """Test that toggle_task_completion displays error for non-existent ID (US2).

    Validates FR-008: System MUST display error message "✗ Error: Task #{id} not found".
    Validates SC-005: Clear error messages for users.
    """
    # Arrange: Create some tasks
    add_task("Task 1", "First")
    capsys.readouterr()  # Clear output

    # Act & Assert: Attempt to toggle non-existent task
    with pytest.raises(ValueError):
        toggle_task_completion(999)

    # Assert: Error message displayed
    captured = capsys.readouterr()
    assert "✗ Error: Task #999 not found" in captured.out


def test_toggle_non_existent_id_does_not_modify_storage():
    """Test that failed toggle doesn't modify storage (US2).

    Validates FR-009: No state changes when error occurs.
    Validates SC-005: No state corruption on error.
    """
    # Arrange: Create tasks and capture initial state
    task1 = add_task("Task 1", "First")
    task2 = add_task("Task 2", "Second")

    initial_count = len(_tasks)
    initial_task1_completed = task1['completed']
    initial_task2_completed = task2['completed']

    # Act: Attempt to toggle non-existent task
    with pytest.raises(ValueError):
        toggle_task_completion(999)

    # Assert: Storage unchanged
    assert len(_tasks) == initial_count

    # Assert: Existing tasks unmodified
    task1_in_storage = next((t for t in _tasks if t.id == task1['id']), None)
    task2_in_storage = next((t for t in _tasks if t.id == task2['id']), None)

    assert task1_in_storage.completed == initial_task1_completed
    assert task2_in_storage.completed == initial_task2_completed
