"""Unit tests for add_task feature (001-add-task).

Tests follow TDD RED-GREEN-REFACTOR cycle per constitution.
These tests should FAIL initially (RED phase) before implementation (GREEN phase).
"""
from datetime import datetime
import pytest
from src.task_manager import add_task
from src.storage import _tasks, _task_id_counter


def test_add_task_with_title_only():
    """Test adding a task with only a title (US1).

    Validates FR-001, FR-004, FR-005, FR-007.
    """
    task = add_task("Buy groceries")

    assert task['id'] == 1
    assert task['title'] == "Buy groceries"
    assert task['description'] is None
    assert task['completed'] is False
    assert isinstance(task['created_at'], datetime)


def test_task_ids_are_sequential():
    """Test that task IDs increment sequentially (US1).

    Validates FR-004 (unique sequential IDs starting from 1).
    """
    task1 = add_task("Task 1")
    task2 = add_task("Task 2")
    task3 = add_task("Task 3")

    assert task1['id'] == 1
    assert task2['id'] == 2
    assert task3['id'] == 3


def test_task_stored_in_memory():
    """Test that tasks are stored in _tasks list (US1).

    Validates FR-006 (in-memory storage).
    """
    initial_count = len(_tasks)

    add_task("Test task")

    assert len(_tasks) == initial_count + 1
    assert _tasks[-1].title == "Test task"


def test_add_task_empty_title_raises_error():
    """Test that empty title raises ValueError (US3).

    Validates FR-002, FR-008, FR-009.
    """
    with pytest.raises(ValueError, match="Task title is required"):
        add_task("")


def test_add_task_none_title_raises_error():
    """Test that None title raises ValueError (US3).

    Validates FR-002, FR-008, FR-009.
    """
    with pytest.raises(ValueError, match="Task title is required"):
        add_task(None)


def test_add_task_whitespace_title_raises_error():
    """Test that whitespace-only title raises ValueError (US3).

    Validates FR-002, FR-008, FR-009.
    """
    with pytest.raises(ValueError, match="Task title is required"):
        add_task("   ")


def test_add_task_with_description():
    """Test adding a task with title and description (US2).

    Validates FR-003, FR-005, FR-007.
    """
    task = add_task("Write report", "Quarterly performance report for Q4")

    assert task['title'] == "Write report"
    assert task['description'] == "Quarterly performance report for Q4"
    assert task['completed'] is False
    assert isinstance(task['created_at'], datetime)


def test_add_task_with_empty_description():
    """Test that empty string description is accepted (US2).

    Validates FR-003 (accepts any string including empty).
    """
    task = add_task("Review code", "")

    assert task['title'] == "Review code"
    assert task['description'] == ""  # Empty string is valid
    assert task['completed'] is False


def test_add_task_very_long_title():
    """Test that system accepts very long titles (Edge Case).

    Validates assumption: no imposed character limits per spec.
    """
    long_title = "A" * 1000  # 1000 character title

    task = add_task(long_title)

    assert task['title'] == long_title
    assert len(task['title']) == 1000


def test_add_task_unicode_characters():
    """Test that system accepts Unicode characters in title (Edge Case).

    Validates: system should accept any valid Python string.
    """
    task = add_task("你好世界 Hello World")

    assert task['title'] == "你好世界 Hello World"
    assert task['completed'] is False


def test_add_task_special_characters_emoji():
    """Test that system accepts special characters and emoji (Edge Case).

    Validates: system should accept any valid Python string.
    """
    task = add_task("Buy groceries 🛒🥕🍞", "Shopping list 📝")

    assert task['title'] == "Buy groceries 🛒🥕🍞"
    assert task['description'] == "Shopping list 📝"


def test_add_task_performance():
    """Test that task creation completes within 10ms (Performance Test).

    Validates SC-001: task creation within <10ms.
    """
    import time

    start_time = time.perf_counter()
    add_task("Performance test task")
    end_time = time.perf_counter()

    elapsed_ms = (end_time - start_time) * 1000
    assert elapsed_ms < 10, f"Task creation took {elapsed_ms:.2f}ms, expected <10ms"


def test_task_timestamp_accuracy():
    """Test that task timestamp is accurate to the second (Timestamp Validation).

    Validates SC-006: timestamps accurate to the second.
    """
    before = datetime.now()
    task = add_task("Timestamp test")
    after = datetime.now()

    # Verify timestamp is between before and after
    assert before <= task['created_at'] <= after

    # Verify timestamp difference is less than 1 second
    time_diff = (after - before).total_seconds()
    assert time_diff < 1, f"Time difference was {time_diff:.2f}s, expected <1s"

    # Verify timestamp is datetime type
    assert isinstance(task['created_at'], datetime)
