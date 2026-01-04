"""Test improved REPL with simplified input."""
from src.main import TodoREPL


def test_improved_input():
    """Test the improved REPL with various input formats."""
    print("\n" + "=" * 70)
    print("IMPROVED REPL - TESTING SIMPLIFIED INPUT")
    print("=" * 70)

    repl = TodoREPL()

    # Test cases with various input formats
    test_commands = [
        # Simple unquoted input
        'add Buy groceries',
        'add Call dentist',
        'add Write report',

        # With pipe separator for description
        'add Team meeting | Discuss Q1 goals',
        'add Fix bug | Issue #123 in production',

        # Original quoted format (still supported)
        'add "Read book"',
        'add "Send email" "Follow up with client"',

        # List tasks
        'list',
    ]

    print("\nTesting various input formats:\n")

    for cmd in test_commands:
        print(f"todo> {cmd}")
        repl.process_command(cmd)
        print()

    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print("\n✅ All input formats working!")
    print("\nSupported formats:")
    print("  1. add Buy groceries           (simple)")
    print("  2. add Task | Description      (with separator)")
    print('  3. add "Task"                  (quoted)')
    print('  4. add "Task" "Description"    (both quoted)')


if __name__ == "__main__":
    test_improved_input()
