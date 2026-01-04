"""Demo script to test Add Task functionality."""
from src.task_manager import add_task, get_all_tasks, clear_all_tasks


def test_add_task():
    """Demonstrate the Add Task feature."""
    print("\n" + "="*60)
    print("TODO APP - FUNCTIONALITY DEMO")
    print("="*60)

    # Clear any existing tasks
    clear_all_tasks()

    # Test Case 1: Add task with title only
    print("\n--- Test Case 1: Add task with title only ---")
    try:
        task1 = add_task("Buy groceries")
        print(f"✓ Task #{task1['id']} added: {task1['title']}")
        print(f"  Description: {task1['description']}")
        print(f"  Completed: {task1['completed']}")
        print(f"  Created: {task1['created_at']}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Test Case 2: Add task with title and description
    print("\n--- Test Case 2: Add task with title and description ---")
    try:
        task2 = add_task("Write report", "Quarterly performance report for Q4")
        print(f"✓ Task #{task2['id']} added: {task2['title']}")
        print(f"  Description: {task2['description']}")
        print(f"  Completed: {task2['completed']}")
        print(f"  Created: {task2['created_at']}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Test Case 3: Add another task
    print("\n--- Test Case 3: Add another task ---")
    try:
        task3 = add_task("Call dentist", "Schedule annual checkup")
        print(f"✓ Task #{task3['id']} added: {task3['title']}")
        print(f"  Description: {task3['description']}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Test Case 4: Try to add task with empty title (should fail)
    print("\n--- Test Case 4: Empty title (should fail) ---")
    try:
        task4 = add_task("")
        print(f"✓ Task #{task4['id']} added: {task4['title']}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Test Case 5: Try to add task with None title (should fail)
    print("\n--- Test Case 5: None title (should fail) ---")
    try:
        task5 = add_task(None)
        print(f"✓ Task #{task5['id']} added: {task5['title']}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Display all tasks
    print("\n" + "="*60)
    print("ALL TASKS IN MEMORY")
    print("="*60)
    tasks = get_all_tasks()
    print(f"\nTotal tasks: {len(tasks)}")

    for task in tasks:
        status = "✓" if task.completed else "○"
        print(f"\n{status} Task #{task.id}: {task.title}")
        if task.description:
            print(f"  Description: {task.description}")
        print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)


if __name__ == "__main__":
    test_add_task()
