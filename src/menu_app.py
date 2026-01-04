"""Todo App - Menu-Driven Interface.

This module provides a numbered menu interface for the Todo application,
matching the design specification provided by the user.
"""
import sys
from typing import NoReturn

from .storage import TaskStore


class TodoMenuApp:
    """Menu-driven Todo Application.

    Provides an interactive numbered menu interface (1-8) for managing tasks.
    """

    def __init__(self) -> None:
        """Initialize the menu app with a task store."""
        self.store = TaskStore()
        self.running = True

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("TODO APPLICATION")
        print("=" * 50)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Completion")
        print("6. Search / Filter Tasks")
        print("7. Sort Tasks")
        print("8. Exit")
        print("=" * 50)

    def handle_add_task(self) -> None:
        """Handle option 1: Add Task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("✗ Error: Task title is required")
            return

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        try:
            task = self.store.add_task(title, description)
            print(f"\n✓ Task #{task['id']} added: {task['title']}")
        except ValueError as e:
            print(f"\n✗ Error: {e}")

    def handle_view_all_tasks(self) -> None:
        """Handle option 2: View All Tasks."""
        tasks = self.store.get_all_tasks()

        if not tasks:
            print("\nNo tasks found.")
            return

        print(f"\n--- All Tasks ({len(tasks)}) ---")
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"\n{status} Task #{task.id}: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
            print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Status: {'Completed' if task.completed else 'Incomplete'}")

    def handle_update_task(self) -> None:
        """Handle option 3: Update Task."""
        print("\n--- Update Task ---")

        try:
            task_id = int(input("Enter task ID to update: ").strip())
        except ValueError:
            print("✗ Error: Invalid task ID")
            return

        # Check if task exists
        task = self.store.get_task_by_id(task_id)
        if task is None:
            print(f"✗ Error: Task #{task_id} not found")
            return

        print(f"\nCurrent task: {task.title}")
        if task.description:
            print(f"Description: {task.description}")

        print("\nWhat would you like to update?")
        print("1. Title")
        print("2. Description")
        print("3. Both")

        choice = input("Enter choice (1-3): ").strip()

        title = None
        description = None

        if choice in ["1", "3"]:
            title = input("Enter new title: ").strip()
            if not title:
                print("✗ Error: Title cannot be empty")
                return

        if choice in ["2", "3"]:
            description = input("Enter new description (or press Enter to keep current): ").strip()
            if not description and choice == "2":
                description = input("Enter new description: ").strip()

        try:
            updated = self.store.update_task(task_id, title=title, description=description if choice in ["2", "3"] else None)
            print(f"\n✓ Task #{updated['id']} updated successfully")
        except ValueError as e:
            print(f"\n✗ Error: {e}")

    def handle_delete_task(self) -> None:
        """Handle option 4: Delete Task."""
        print("\n--- Delete Task ---")

        try:
            task_id = int(input("Enter task ID to delete: ").strip())
        except ValueError:
            print("✗ Error: Invalid task ID")
            return

        # Confirm deletion
        task = self.store.get_task_by_id(task_id)
        if task is None:
            print(f"✗ Error: Task #{task_id} not found")
            return

        confirm = input(f"Are you sure you want to delete '{task.title}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled")
            return

        try:
            deleted = self.store.delete_task(task_id)
            print(f"\n✓ Task #{deleted['id']} deleted: {deleted['title']}")
        except ValueError as e:
            print(f"\n✗ Error: {e}")

    def handle_toggle_completion(self) -> None:
        """Handle option 5: Toggle Task Completion."""
        print("\n--- Toggle Task Completion ---")

        try:
            task_id = int(input("Enter task ID: ").strip())
        except ValueError:
            print("✗ Error: Invalid task ID")
            return

        try:
            task = self.store.toggle_task_completion(task_id)
            if task['completed']:
                print(f"\n✓ Task #{task['id']} marked as complete")
            else:
                print(f"\n✓ Task #{task['id']} marked as incomplete")
        except ValueError as e:
            print(f"\n✗ Error: {e}")

    def handle_search_filter(self) -> None:
        """Handle option 6: Search / Filter Tasks."""
        print("\n--- Search / Filter Tasks ---")

        keyword = input("Enter search keyword (or press Enter to skip): ").strip()
        keyword = keyword if keyword else None

        print("\nFilter by status:")
        print("1. All tasks")
        print("2. Completed only")
        print("3. Incomplete only")

        filter_choice = input("Enter choice (1-3): ").strip()

        status_filter = "all"
        if filter_choice == "2":
            status_filter = "completed"
        elif filter_choice == "3":
            status_filter = "incomplete"

        results = self.store.search_tasks(keyword=keyword, status_filter=status_filter)

        if not results:
            print("\nNo tasks found matching your criteria.")
            return

        print(f"\n--- Search Results ({len(results)}) ---")
        for task in results:
            status = "✓" if task.completed else "○"
            print(f"\n{status} Task #{task.id}: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
            print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Status: {'Completed' if task.completed else 'Incomplete'}")

    def handle_sort_tasks(self) -> None:
        """Handle option 7: Sort Tasks."""
        print("\n--- Sort Tasks ---")
        print("Sort by:")
        print("1. ID (default)")
        print("2. Title (alphabetical)")
        print("3. Created date")
        print("4. Completion status")

        choice = input("Enter choice (1-4): ").strip()

        sort_by = "id"
        if choice == "2":
            sort_by = "title"
        elif choice == "3":
            sort_by = "created"
        elif choice == "4":
            sort_by = "status"

        reverse = input("Reverse order? (y/n): ").strip().lower() == 'y'

        tasks = self.store.get_sorted_tasks(sort_by=sort_by, reverse=reverse)

        if not tasks:
            print("\nNo tasks to display.")
            return

        print(f"\n--- Sorted Tasks ({len(tasks)}) ---")
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"\n{status} Task #{task.id}: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
            print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Status: {'Completed' if task.completed else 'Incomplete'}")

    def handle_exit(self) -> None:
        """Handle option 8: Exit."""
        self.running = False
        print("\nGoodbye! All tasks will be lost (in-memory only).")

    def run(self) -> None:
        """Start the menu-driven application."""
        print("\nWelcome to the Todo Application!")

        while self.running:
            self.display_menu()

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_all_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_toggle_completion()
            elif choice == "6":
                self.handle_search_filter()
            elif choice == "7":
                self.handle_sort_tasks()
            elif choice == "8":
                self.handle_exit()
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 8.")

            if self.running:
                input("\nPress Enter to continue...")


def main() -> NoReturn:
    """Main entry point for the menu-driven Todo application."""
    app = TodoMenuApp()
    app.run()
    sys.exit(0)


if __name__ == "__main__":
    main()
