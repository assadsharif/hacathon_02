"""REPL Demo Script.

Demonstrates the REPL interface with simulated commands.
"""
from src.main import TodoREPL


def demo_repl():
    """Demonstrate REPL functionality with sample commands."""
    print("\n" + "=" * 70)
    print("TODO APP - REPL DEMO")
    print("=" * 70)

    repl = TodoREPL()

    # Simulate commands
    commands = [
        'add "Buy groceries"',
        'add "Write report" "Quarterly performance report for Q4"',
        'add "Call dentist" "Schedule annual checkup"',
        'list',
        'add ""',  # Test error handling
        'add "Meeting with team"',
        'list',
    ]

    print("\nSimulating user commands:\n")

    for cmd in commands:
        print(f"todo> {cmd}")
        repl.process_command(cmd)
        print()

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nTo run interactively: python3 main.py")
    print("or: uv run python main.py")


if __name__ == "__main__":
    demo_repl()
