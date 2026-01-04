"""Todo App - REPL Console Interface.

This module provides the command-line REPL interface for the Todo application,
following the specification at /specs/phase1/features/add-task.md.
"""
import shlex
import sys
from typing import NoReturn

from .storage import TaskStore


class TodoREPL:
    """Read-Eval-Print Loop for Todo App.

    Provides an interactive command-line interface for managing tasks.
    """

    def __init__(self) -> None:
        """Initialize the REPL with a task store."""
        self.store = TaskStore()
        self.running = True

    def display_welcome(self) -> None:
        """Display welcome message and instructions."""
        print("\n" + "=" * 70)
        print("TODO APP - In-Memory Console (REPL)")
        print("=" * 70)
        print("\nAvailable Commands:")
        print("  add <title> [| description]  - Add a new task")
        print("  list                         - List all tasks")
        print("  delete <id>                  - Delete a task")
        print("  update <id> <field> <value>  - Update a task")
        print("  complete <id>                - Toggle task completion")
        print("  help                         - Show this help message")
        print("  exit                         - Exit the application")
        print("\nExamples:")
        print('  add Buy groceries')
        print('  add Team meeting | Discuss Q1 goals')
        print('  list')
        print('  complete 1')
        print('  update 1 title New task name')
        print('  update 1 description New description')
        print('  delete 1')
        print("=" * 70)

    def parse_command(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments.

        Uses shlex to properly handle quoted strings.

        Args:
            user_input: Raw user input string

        Returns:
            Tuple of (command, arguments_list)
        """
        try:
            tokens = shlex.split(user_input)
        except ValueError as e:
            # Handle unclosed quotes
            raise ValueError(f"Parse error: {e}")

        if not tokens:
            return ("", [])

        command = tokens[0].lower()
        args = tokens[1:]
        return (command, args)

    def handle_add(self, args: list[str], raw_input: str = "") -> None:
        """Handle the 'add' command.

        Implements AC5 and AC6 from the specification.
        Supports both quoted and unquoted input for better UX.

        Args:
            args: List of arguments [title, description (optional)]
            raw_input: Original user input for fallback parsing
        """
        if len(args) == 0:
            print("✗ Error: Missing task title")
            print('Usage: add <title> [| description]')
            print('Examples:')
            print('  add Buy groceries')
            print('  add Write report | Quarterly performance')
            return

        # If using quoted args, use them directly
        if len(args) >= 1:
            title = args[0]
            description = args[1] if len(args) > 1 else None
        else:
            # Fallback: shouldn't reach here but handle gracefully
            title = " ".join(args)
            description = None

        try:
            task = self.store.add_task(title, description)
            # AC5: Confirmation message format
            print(f"✓ Task #{task['id']} added: {task['title']}")
        except ValueError as e:
            # AC6: Error handling
            print(f"✗ Error: {e}")

    def handle_list(self) -> None:
        """Handle the 'list' command.

        Displays all tasks in the in-memory storage.
        """
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

    def handle_delete(self, args: list[str]) -> None:
        """Handle the 'delete' command.

        Args:
            args: List of arguments [task_id]
        """
        if len(args) == 0:
            print("✗ Error: Missing task ID")
            print('Usage: delete <task_id>')
            print('Example: delete 1')
            return

        try:
            task_id = int(args[0])
            task = self.store.delete_task(task_id)
            print(f"✓ Task #{task['id']} deleted: {task['title']}")
        except ValueError as e:
            if "not found" in str(e):
                print(f"✗ Error: {e}")
            else:
                print("✗ Error: Invalid task ID")

    def handle_update(self, args: list[str], raw_input: str = "") -> None:
        """Handle the 'update' command.

        Args:
            args: List of arguments [task_id, field, value...]
            raw_input: Original input for parsing value
        """
        if len(args) < 3:
            print("✗ Error: Missing required arguments")
            print('Usage: update <task_id> <field> <value>')
            print('Fields: title, description')
            print('Examples:')
            print('  update 1 title New task name')
            print('  update 1 description New description')
            return

        try:
            task_id = int(args[0])
            field = args[1].lower()

            # Get the value (everything after field)
            # Find position of field in raw_input and take everything after it
            update_prefix = f"update {args[0]} {args[1]} "
            if raw_input.lower().startswith("update "):
                remainder = raw_input[7:].strip()  # Remove "update "
                parts = remainder.split(None, 2)  # Split into [id, field, value]
                if len(parts) >= 3:
                    value = parts[2]
                else:
                    value = " ".join(args[2:])
            else:
                value = " ".join(args[2:])

            if field == "title":
                task = self.store.update_task(task_id, title=value)
                print(f"✓ Task #{task['id']} updated")
            elif field == "description":
                task = self.store.update_task(task_id, description=value)
                print(f"✓ Task #{task['id']} updated")
            else:
                print(f"✗ Error: Unknown field '{field}'")
                print("Valid fields: title, description")

        except ValueError as e:
            if "Invalid" in str(e) or "not a number" in str(e).lower():
                print("✗ Error: Invalid task ID")
            else:
                print(f"✗ Error: {e}")

    def handle_complete(self, args: list[str]) -> None:
        """Handle the 'complete' command.

        Args:
            args: List of arguments [task_id]
        """
        if len(args) == 0:
            print("✗ Error: Missing task ID")
            print('Usage: complete <task_id>')
            print('Example: complete 1')
            return

        try:
            task_id = int(args[0])
            task = self.store.toggle_task_completion(task_id)

            if task['completed']:
                print(f"✓ Task #{task['id']} marked as complete")
            else:
                print(f"✓ Task #{task['id']} marked as incomplete")

        except ValueError as e:
            if "not found" in str(e):
                print(f"✗ Error: {e}")
            else:
                print("✗ Error: Invalid task ID")

    def handle_help(self) -> None:
        """Display help information."""
        self.display_welcome()

    def handle_exit(self) -> None:
        """Handle exit command."""
        self.running = False
        print("\nGoodbye! All tasks will be lost (in-memory only).")

    def process_command(self, user_input: str) -> None:
        """Process a single command.

        Args:
            user_input: Raw user input string
        """
        try:
            # Special handling for 'add' command to support unquoted input
            if user_input.lower().startswith("add "):
                # Extract everything after "add "
                remainder = user_input[4:].strip()

                if not remainder:
                    self.handle_add([])
                    return

                # Check for pipe separator for description
                if "|" in remainder:
                    parts = remainder.split("|", 1)
                    title = parts[0].strip()
                    description = parts[1].strip()
                    self.handle_add([title, description])
                elif '"' in remainder:
                    # If there are quotes, use shlex to parse properly
                    try:
                        tokens = shlex.split(remainder)
                        self.handle_add(tokens)
                    except ValueError:
                        # If shlex fails, treat entire remainder as title
                        self.handle_add([remainder])
                else:
                    # No quotes, no pipe: treat entire remainder as title
                    self.handle_add([remainder])
                return

            # Special handling for 'update' command to preserve multi-word values
            if user_input.lower().startswith("update "):
                remainder = user_input[7:].strip()
                parts = remainder.split(None, 2)  # Split into [id, field, value]
                if len(parts) >= 3:
                    self.handle_update(parts, user_input)
                else:
                    self.handle_update(parts if parts else [], user_input)
                return

            # For other commands, use standard parsing
            command, args = self.parse_command(user_input)

            if command == "":
                return
            elif command == "add":
                self.handle_add(args, user_input)
            elif command == "list":
                self.handle_list()
            elif command == "delete":
                self.handle_delete(args)
            elif command == "update":
                self.handle_update(args, user_input)
            elif command == "complete" or command == "done":
                self.handle_complete(args)
            elif command == "help":
                self.handle_help()
            elif command == "exit" or command == "quit":
                self.handle_exit()
            else:
                print(f"✗ Unknown command: {command}")
                print("Type 'help' for available commands.")

        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    def run(self) -> None:
        """Start the REPL loop."""
        self.display_welcome()

        while self.running:
            try:
                user_input = input("\ntodo> ").strip()
                if user_input:
                    self.process_command(user_input)
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'exit' to quit.")
            except EOFError:
                print("\n")
                self.handle_exit()
                break


def main() -> NoReturn:
    """Main entry point for the Todo application."""
    repl = TodoREPL()
    repl.run()
    sys.exit(0)


if __name__ == "__main__":
    main()
