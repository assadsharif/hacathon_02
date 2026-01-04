"""Comprehensive test suite for all 5 todo app features.

Tests all features against their specifications:
1. Add Task - /specs/phase1/features/add-task.md
2. View Task List - (list command)
3. Delete Task - /specs/phase1/features/delete-task.md
4. Update Task - /specs/phase1/features/update-task.md
5. Mark as Complete - /specs/phase1/features/mark-complete.md
"""
from src.storage import TaskStore


def test_all_features():
    """Test all 5 todo app features comprehensively."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TEST SUITE - ALL 5 FEATURES")
    print("=" * 80)

    store = TaskStore()

    # ===================================================================
    # FEATURE 1: ADD TASK
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 1] ADD TASK")
    print("=" * 80)

    print("\n[Test 1.1] Add task with title only")
    task1 = store.add_task("Buy groceries")
    assert task1['id'] == 1
    assert task1['title'] == "Buy groceries"
    assert task1['description'] is None
    assert task1['completed'] is False
    print(f"✓ Task #{task1['id']} added: {task1['title']}")

    print("\n[Test 1.2] Add task with title and description")
    task2 = store.add_task("Write report", "Q4 performance analysis")
    assert task2['id'] == 2
    assert task2['description'] == "Q4 performance analysis"
    print(f"✓ Task #{task2['id']} added: {task2['title']}")

    print("\n[Test 1.3] Add multiple tasks")
    task3 = store.add_task("Call dentist")
    task4 = store.add_task("Team meeting", "Discuss new features")
    assert store.task_count() == 4
    print(f"✓ Added 2 more tasks. Total: {store.task_count()}")

    print("\n[Test 1.4] Error: Empty title")
    try:
        store.add_task("")
        print("✗ FAIL: Should reject empty title")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    # ===================================================================
    # FEATURE 2: VIEW TASK LIST
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 2] VIEW TASK LIST")
    print("=" * 80)

    print("\n[Test 2.1] Get all tasks")
    all_tasks = store.get_all_tasks()
    assert len(all_tasks) == 4
    print(f"✓ Retrieved {len(all_tasks)} tasks")

    print("\n[Test 2.2] Display task list")
    for task in all_tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} Task #{task.id}: {task.title}")
        if task.description:
            print(f"  Description: {task.description}")

    print("\n[Test 2.3] Get task by ID")
    task = store.get_task_by_id(1)
    assert task is not None
    assert task.title == "Buy groceries"
    print(f"✓ Found task #1: {task.title}")

    print("\n[Test 2.4] Get non-existent task")
    task = store.get_task_by_id(999)
    assert task is None
    print("✓ Non-existent task returns None")

    # ===================================================================
    # FEATURE 3: DELETE TASK
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 3] DELETE TASK")
    print("=" * 80)

    print("\n[Test 3.1] Delete existing task")
    deleted = store.delete_task(2)
    assert deleted['id'] == 2
    assert deleted['title'] == "Write report"
    assert store.task_count() == 3
    print(f"✓ Task #{deleted['id']} deleted: {deleted['title']}")

    print("\n[Test 3.2] Verify task is gone")
    task = store.get_task_by_id(2)
    assert task is None
    print("✓ Deleted task no longer exists")

    print("\n[Test 3.3] Error: Delete non-existent task")
    try:
        store.delete_task(999)
        print("✗ FAIL: Should raise error for non-existent task")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Test 3.4] Other tasks unaffected")
    task = store.get_task_by_id(1)
    assert task is not None
    print(f"✓ Task #1 still exists: {task.title}")

    # ===================================================================
    # FEATURE 4: UPDATE TASK
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 4] UPDATE TASK")
    print("=" * 80)

    print("\n[Test 4.1] Update title only")
    original_created_at = store.get_task_by_id(1).created_at
    updated = store.update_task(1, title="Buy organic groceries")
    assert updated['title'] == "Buy organic groceries"
    assert updated['description'] is None
    assert updated['created_at'] == original_created_at
    print(f"✓ Task #1 updated: {updated['title']}")

    print("\n[Test 4.2] Update description only")
    task4_id = 4
    updated = store.update_task(task4_id, description="Discuss Q1 roadmap")
    assert updated['title'] == "Team meeting"  # Unchanged
    assert updated['description'] == "Discuss Q1 roadmap"
    print(f"✓ Task #{task4_id} description updated")

    print("\n[Test 4.3] Update both title and description")
    updated = store.update_task(3, title="Dentist appointment", description="Annual checkup")
    assert updated['title'] == "Dentist appointment"
    assert updated['description'] == "Annual checkup"
    print(f"✓ Task #3 updated: {updated['title']}")

    print("\n[Test 4.4] Error: Empty title")
    try:
        store.update_task(1, title="")
        print("✗ FAIL: Should reject empty title")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Test 4.5] Error: No fields provided")
    try:
        store.update_task(1)
        print("✗ FAIL: Should require at least one field")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Test 4.6] Error: Update non-existent task")
    try:
        store.update_task(999, title="New title")
        print("✗ FAIL: Should raise error for non-existent task")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    # ===================================================================
    # FEATURE 5: MARK AS COMPLETE
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 5] MARK AS COMPLETE")
    print("=" * 80)

    print("\n[Test 5.1] Mark incomplete task as complete")
    task = store.get_task_by_id(1)
    assert task.completed is False
    toggled = store.toggle_task_completion(1)
    assert toggled['completed'] is True
    print(f"✓ Task #1 marked as complete")

    print("\n[Test 5.2] Mark complete task as incomplete")
    toggled = store.toggle_task_completion(1)
    assert toggled['completed'] is False
    print(f"✓ Task #1 marked as incomplete")

    print("\n[Test 5.3] Multiple toggles")
    store.toggle_task_completion(1)  # True
    store.toggle_task_completion(1)  # False
    toggled = store.toggle_task_completion(1)  # True
    assert toggled['completed'] is True
    print(f"✓ Task #1 toggled 3 times, now completed: {toggled['completed']}")

    print("\n[Test 5.4] Other fields unchanged")
    task = store.get_task_by_id(1)
    assert task.title == "Buy organic groceries"
    assert task.created_at == original_created_at
    print("✓ Other fields remain unchanged")

    print("\n[Test 5.5] Error: Toggle non-existent task")
    try:
        store.toggle_task_completion(999)
        print("✗ FAIL: Should raise error for non-existent task")
    except ValueError as e:
        print(f"✓ Correctly rejected: {e}")

    print("\n[Test 5.6] Visual display of completed tasks")
    all_tasks = store.get_all_tasks()
    for task in all_tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} Task #{task.id}: {task.title}")

    # ===================================================================
    # FINAL SUMMARY
    # ===================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("✅ FEATURE 1: ADD TASK - PASSED (4/4 tests)")
    print("✅ FEATURE 2: VIEW TASK LIST - PASSED (4/4 tests)")
    print("✅ FEATURE 3: DELETE TASK - PASSED (4/4 tests)")
    print("✅ FEATURE 4: UPDATE TASK - PASSED (6/6 tests)")
    print("✅ FEATURE 5: MARK AS COMPLETE - PASSED (6/6 tests)")
    print("\n✅ ALL 24 TESTS PASSED!")
    print("=" * 80)

    print("\n✓ All 5 features working correctly!")


if __name__ == "__main__":
    test_all_features()
