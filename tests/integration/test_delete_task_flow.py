"""Integration tests for delete_task feature (003-delete-task).

Tests verify delete_task integrates correctly with add_task and storage system.
Tests validate ID generation, multi-operation flows, and data consistency.
"""
from datetime import datetime
import pytest
from src.task_manager import add_task, delete_task
from src.storage import _tasks, _task_id_counter


def test_delete_task_works_with_add_task():
    """Test that delete_task correctly integrates with add_task (Integration).

    Validates full workflow: add multiple tasks → delete one → verify storage state.
    Validates SC-004: Deletion of one task does not affect other tasks.
    """
    # Arrange: Create multiple tasks using add_task
    task1 = add_task("Task 1", "First task")
    task2 = add_task("Task 2", "Second task")
    task3 = add_task("Task 3", "Third task")

    task1_id = task1['id']
    task2_id = task2['id']
    task3_id = task3['id']

    initial_count = len(_tasks)

    # Act: Delete middle task
    deleted = delete_task(task2_id)

    # Assert: Deleted task data matches what was added
    assert deleted['id'] == task2_id
    assert deleted['title'] == "Task 2"
    assert deleted['description'] == "Second task"
    assert deleted['completed'] is False
    assert isinstance(deleted['created_at'], datetime)

    # Assert: Storage correctly updated
    assert len(_tasks) == initial_count - 1
    assert len(_tasks) == 2

    # Assert: Other tasks unaffected
    remaining_tasks = {t.id: t for t in _tasks}
    assert task1_id in remaining_tasks
    assert task2_id not in remaining_tasks
    assert task3_id in remaining_tasks

    # Assert: Remaining tasks have original data
    assert remaining_tasks[task1_id].title == "Task 1"
    assert remaining_tasks[task1_id].description == "First task"
    assert remaining_tasks[task3_id].title == "Task 3"
    assert remaining_tasks[task3_id].description == "Third task"


def test_deleted_ids_are_not_reused():
    """Test that deleted task IDs are never reused (Integration).

    Validates ID generation behavior: counter only increments, never reuses deleted IDs.
    Validates ADR-0003: Sequential counter-based ID generation.
    """
    # Arrange: Create tasks and capture IDs
    task1 = add_task("Task 1", "First")
    task2 = add_task("Task 2", "Second")
    task3 = add_task("Task 3", "Third")

    task1_id = task1['id']
    task2_id = task2['id']
    task3_id = task3['id']

    # Act: Delete task 2 (middle ID)
    delete_task(task2_id)

    # Act: Create new tasks after deletion
    task4 = add_task("Task 4", "Fourth")
    task5 = add_task("Task 5", "Fifth")

    # Assert: New IDs are higher than all previous IDs (including deleted)
    assert task4['id'] > task3_id
    assert task5['id'] > task4['id']

    # Assert: Deleted ID not reused
    all_current_ids = [t.id for t in _tasks]
    assert task2_id not in all_current_ids
    assert task1_id in all_current_ids
    assert task3_id in all_current_ids
    assert task4['id'] in all_current_ids
    assert task5['id'] in all_current_ids

    # Assert: IDs are sequential from original counter
    assert task4['id'] == task3_id + 1
    assert task5['id'] == task4['id'] + 1


# ============================================================================
# NOTE: T041 test_delete_task_works_with_toggled_task BLOCKED
# ============================================================================
# Cannot implement T041 because toggle_task_completion function doesn't exist yet.
# The 002-mark-complete feature has not been implemented.
# This test should be implemented when toggle_task_completion becomes available.
#
# Expected test behavior:
#   1. Add task
#   2. Toggle task to completed=True
#   3. Delete the completed task
#   4. Verify deleted task data shows completed=True
#   5. Verify storage correctly reflects deletion


# ============================================================================
# Performance Testing
# ============================================================================

def test_delete_task_performance():
    """Test that delete_task completes in under 10ms (Performance).

    Validates SC-006: Delete operation completes in under 10ms.
    Tests with 100 tasks to ensure performance at scale.
    """
    import time

    # Arrange: Create 100 tasks
    tasks = []
    for i in range(100):
        task = add_task(f"Task {i}", f"Description {i}")
        tasks.append(task)

    # Select middle task for deletion (worst case for linear search)
    target_task_id = tasks[50]['id']

    # Act: Measure deletion time
    start_time = time.perf_counter()
    deleted = delete_task(target_task_id)
    end_time = time.perf_counter()

    # Calculate elapsed time in milliseconds
    elapsed_ms = (end_time - start_time) * 1000

    # Assert: Deletion completed successfully
    assert deleted['id'] == target_task_id
    assert deleted['title'] == "Task 50"

    # Assert: Performance meets SC-006 requirement (<10ms)
    assert elapsed_ms < 10.0, f"Delete took {elapsed_ms:.2f}ms, expected <10ms"

    # Assert: Storage correctly updated
    assert len(_tasks) == 99
    assert not any(t.id == target_task_id for t in _tasks)
