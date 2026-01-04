"""Complete demo of all 5 todo app features.

Demonstrates all features through the REPL interface:
1. Add Task
2. View Task List
3. Delete Task
4. Update Task
5. Mark as Complete
"""
from src.main import TodoREPL


def demo_all_features():
    """Demonstrate all 5 features with realistic workflow."""
    print("\n" + "=" * 80)
    print("TODO APP - COMPLETE FEATURE DEMONSTRATION")
    print("=" * 80)
    print("\nThis demo showcases all 5 features of the Todo App:\n")
    print("  1. Add Task")
    print("  2. View Task List")
    print("  3. Delete Task")
    print("  4. Update Task")
    print("  5. Mark as Complete")
    print("=" * 80)

    repl = TodoREPL()

    commands = [
        # FEATURE 1: ADD TASK
        ("=" * 80, False),
        ("[FEATURE 1] ADD TASK - Create new todo items", False),
        ("=" * 80, False),
        ("", False),
        "add Buy groceries",
        "add Call dentist",
        "add Write quarterly report | Q4 performance analysis",
        "add Team meeting | Discuss new product features",
        "add Send emails",
        ("", False),

        # FEATURE 2: VIEW TASK LIST
        ("=" * 80, False),
        ("[FEATURE 2] VIEW TASK LIST - Display all tasks", False),
        ("=" * 80, False),
        ("", False),
        "list",
        ("", False),

        # FEATURE 5: MARK AS COMPLETE
        ("=" * 80, False),
        ("[FEATURE 5] MARK AS COMPLETE - Toggle task completion status", False),
        ("=" * 80, False),
        ("", False),
        "complete 1",
        "complete 5",
        ("", False),
        ("Viewing updated list with completed tasks:", False),
        "list",
        ("", False),

        # FEATURE 4: UPDATE TASK
        ("=" * 80, False),
        ("[FEATURE 4] UPDATE TASK - Modify existing task details", False),
        ("=" * 80, False),
        ("", False),
        "update 2 title Call dentist for annual checkup",
        "update 3 description Q4 2025 performance and goals for 2026",
        "update 4 title Weekly team standup",
        ("", False),
        ("Viewing updated list:", False),
        "list",
        ("", False),

        # FEATURE 3: DELETE TASK
        ("=" * 80, False),
        ("[FEATURE 3] DELETE TASK - Remove tasks from the list", False),
        ("=" * 80, False),
        ("", False),
        "delete 5",
        ("", False),
        ("Viewing final list:", False),
        "list",
        ("", False),

        # FINAL SUMMARY
        ("=" * 80, False),
        ("FINAL STATE OF TODO LIST", False),
        ("=" * 80, False),
        ("", False),
        ("✓ Task #1: Buy groceries (COMPLETED)", False),
        ("○ Task #2: Call dentist for annual checkup", False),
        ("○ Task #3: Write quarterly report (Q4 2025 performance and goals for 2026)", False),
        ("○ Task #4: Weekly team standup (Discuss new product features)", False),
        ("✗ Task #5: Send emails (DELETED)", False),
        ("", False),
        ("=" * 80, False),
        ("ALL 5 FEATURES DEMONSTRATED SUCCESSFULLY!", False),
        ("=" * 80, False),
    ]

    print("\n\nSimulated REPL session:\n")

    for cmd in commands:
        if isinstance(cmd, tuple):
            # Print informational message
            msg, is_command = cmd
            if msg:
                print(msg)
        else:
            # Execute command
            print(f"todo> {cmd}")
            repl.process_command(cmd)
        print()

    print("=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nTo try it yourself, run: python3 main.py")
    print("\nAll commands demonstrated:")
    print("  • add <title>               - Simple add")
    print("  • add <title> | <desc>      - Add with description")
    print("  • list                      - View all tasks")
    print("  • complete <id>             - Toggle completion")
    print("  • update <id> <field> <val> - Update task")
    print("  • delete <id>               - Delete task")


if __name__ == "__main__":
    demo_all_features()
