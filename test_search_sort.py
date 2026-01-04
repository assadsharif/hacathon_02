"""Test suite for Search/Filter and Sort features."""
from src.storage import TaskStore


def test_search_and_sort():
    """Test search/filter and sort features."""
    print("\n" + "=" * 80)
    print("TESTING SEARCH/FILTER AND SORT FEATURES")
    print("=" * 80)

    store = TaskStore()

    # Setup test data
    print("\n[Setup] Adding test tasks...")
    store.add_task("Buy groceries", "Milk, eggs, bread")
    store.add_task("Call dentist", "Schedule annual checkup")
    store.add_task("Buy flowers", "For anniversary")
    store.add_task("Write report", "Q4 performance analysis")
    store.add_task("Team meeting", "Discuss new features")

    # Mark some as complete
    store.toggle_task_completion(1)  # Buy groceries
    store.toggle_task_completion(3)  # Buy flowers

    print("✓ Added 5 tasks (2 completed, 3 incomplete)")

    # ===================================================================
    # FEATURE 6: SEARCH / FILTER
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 6] SEARCH / FILTER TASKS")
    print("=" * 80)

    print("\n[Test 6.1] Search by keyword 'buy'")
    results = store.search_tasks(keyword="buy")
    assert len(results) == 2
    print(f"✓ Found {len(results)} tasks containing 'buy'")
    for task in results:
        print(f"  - Task #{task.id}: {task.title}")

    print("\n[Test 6.2] Search case-insensitive")
    results = store.search_tasks(keyword="BUY")
    assert len(results) == 2
    print(f"✓ Case-insensitive search works: {len(results)} results")

    print("\n[Test 6.3] Search in description")
    results = store.search_tasks(keyword="annual")
    assert len(results) == 1
    assert results[0].title == "Call dentist"
    print(f"✓ Found task by searching description: '{results[0].title}'")

    print("\n[Test 6.4] Filter by completed")
    results = store.search_tasks(status_filter="completed")
    assert len(results) == 2
    print(f"✓ Found {len(results)} completed tasks")
    for task in results:
        status = "✓" if task.completed else "○"
        print(f"  {status} Task #{task.id}: {task.title}")

    print("\n[Test 6.5] Filter by incomplete")
    results = store.search_tasks(status_filter="incomplete")
    assert len(results) == 3
    print(f"✓ Found {len(results)} incomplete tasks")

    print("\n[Test 6.6] Combined search and filter")
    results = store.search_tasks(keyword="buy", status_filter="completed")
    assert len(results) == 2  # Both "buy" tasks are completed
    print(f"✓ Combined search/filter: {len(results)} completed tasks containing 'buy'")

    print("\n[Test 6.7] No matches")
    results = store.search_tasks(keyword="nonexistent")
    assert len(results) == 0
    print("✓ No matches returns empty list")

    # ===================================================================
    # FEATURE 7: SORT TASKS
    # ===================================================================
    print("\n" + "=" * 80)
    print("[FEATURE 7] SORT TASKS")
    print("=" * 80)

    print("\n[Test 7.1] Sort by ID (default)")
    results = store.get_sorted_tasks(sort_by="id")
    ids = [task.id for task in results]
    assert ids == [1, 2, 3, 4, 5]
    print(f"✓ Sorted by ID: {ids}")

    print("\n[Test 7.2] Sort by ID (reverse)")
    results = store.get_sorted_tasks(sort_by="id", reverse=True)
    ids = [task.id for task in results]
    assert ids == [5, 4, 3, 2, 1]
    print(f"✓ Sorted by ID (reverse): {ids}")

    print("\n[Test 7.3] Sort by title (alphabetical)")
    results = store.get_sorted_tasks(sort_by="title")
    titles = [task.title for task in results]
    expected = ["Buy flowers", "Buy groceries", "Call dentist", "Team meeting", "Write report"]
    assert titles == expected
    print(f"✓ Sorted alphabetically:")
    for title in titles:
        print(f"  - {title}")

    print("\n[Test 7.4] Sort by title (reverse)")
    results = store.get_sorted_tasks(sort_by="title", reverse=True)
    titles = [task.title for task in results]
    assert titles == list(reversed(expected))
    print(f"✓ Sorted alphabetically (reverse): First = '{titles[0]}'")

    print("\n[Test 7.5] Sort by created date")
    results = store.get_sorted_tasks(sort_by="created")
    # Should be in order 1-5 since created sequentially
    ids = [task.id for task in results]
    assert ids == [1, 2, 3, 4, 5]
    print(f"✓ Sorted by created date: {ids}")

    print("\n[Test 7.6] Sort by status")
    results = store.get_sorted_tasks(sort_by="status")
    # Incomplete first (2, 4, 5), then completed (1, 3)
    statuses = [(task.id, task.completed) for task in results]
    print(f"✓ Sorted by status (incomplete first):")
    for task_id, completed in statuses:
        status = "✓" if completed else "○"
        print(f"  {status} Task #{task_id}")

    # Verify incomplete tasks come first
    incomplete_tasks = [t for t in results if not t.completed]
    completed_tasks = [t for t in results if t.completed]
    assert len(incomplete_tasks) == 3
    assert len(completed_tasks) == 2
    # All incomplete should come before all completed
    assert all(not t.completed for t in results[:3])
    assert all(t.completed for t in results[3:])
    print("✓ All incomplete tasks before completed tasks")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("✅ FEATURE 6: SEARCH / FILTER - PASSED (7/7 tests)")
    print("✅ FEATURE 7: SORT TASKS - PASSED (6/6 tests)")
    print("\n✅ ALL 13 NEW TESTS PASSED!")
    print("=" * 80)

    print("\n✓ All search/filter and sort features working correctly!")


if __name__ == "__main__":
    test_search_and_sort()
