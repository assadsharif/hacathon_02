# Todo App - Complete Usage Guide

## Overview

A fully-featured, in-memory todo application with 5 core features:

1. ✅ **Add Task** - Create new todo items
2. 📋 **View Task List** - Display all tasks
3. ❌ **Delete Task** - Remove tasks from the list
4. ✏️ **Update Task** - Modify existing task details
5. ✓ **Mark as Complete** - Toggle task completion status

## Quick Start

Run the app:
```bash
python3 main.py
# or
uv run python main.py
```

## Feature 1: Add Task

The app now supports **multiple input formats** for your convenience!

### Format 1: Simple Unquoted Input (Easiest!)
```
todo> add Buy groceries
✓ Task #1 added: Buy groceries

todo> add Call dentist tomorrow
✓ Task #2 added: Call dentist tomorrow
```

**This is the easiest way!** Just type `add` followed by your task. Everything after `add` becomes the task title.

### Format 2: With Description (Using Pipe)
```
todo> add Write report | Quarterly performance for Q4
✓ Task #3 added: Write report
```

Use the pipe symbol `|` to separate title from description:
- Before `|` = Title
- After `|` = Description

### Format 3: Quoted Strings (Advanced)
```
todo> add "Buy groceries"
✓ Task #4 added: Buy groceries

todo> add "Write report" "Quarterly performance"
✓ Task #5 added: Write report
```

## All Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <task>` | Add a new task | `add Buy groceries` |
| `add <task> \| <description>` | Add task with description | `add Meeting \| Discuss Q1` |
| `list` | Show all tasks | `list` |
| `help` | Show help message | `help` |
| `exit` | Quit the app | `exit` |

## Examples

### Adding Simple Tasks
```
todo> add Buy milk
✓ Task #1 added: Buy milk

todo> add Call mom
✓ Task #2 added: Call mom

todo> add Fix bug in app
✓ Task #3 added: Fix bug in app
```

### Adding Tasks with Descriptions
```
todo> add Team meeting | Discuss new features
✓ Task #1 added: Team meeting

todo> add Code review | Review PR #123
✓ Task #2 added: Code review
```

### Viewing All Tasks
```
todo> list

--- All Tasks (2) ---

○ Task #1: Team meeting
  Description: Discuss new features
  Created: 2026-01-04 21:01:05

○ Task #2: Code review
  Description: Review PR #123
  Created: 2026-01-04 21:01:05
```

## Error Handling

### Empty Task
```
todo> add
✗ Error: Missing task title
Usage: add <title> [| description]
```

### Blank Task
```
todo> add
✗ Error: Missing task title
```

## Important Notes

⚠️ **In-Memory Only**: All tasks are stored in memory and will be **lost when you exit** the application. This is by design (no database or file persistence).

✅ **What Works**: All the formats shown above
❌ **What Doesn't Work**: Typing just the task name without `add` command

## Troubleshooting

**Problem**: "Unknown command: my"
**Solution**: You need to use the `add` command:
```
❌ todo> my task
✗ Unknown command: my

✅ todo> add my task
✓ Task #1 added: my task
```

**Problem**: "Missing task title"
**Solution**: Make sure you type something after `add`:
```
❌ todo> add
✗ Error: Missing task title

✅ todo> add Do something
✓ Task #1 added: Do something
```

## Feature 2: View Task List

Display all your tasks with their completion status.

### Command
```
todo> list
```

### Output
```
--- All Tasks (3) ---

✓ Task #1: Buy groceries
  Created: 2026-01-04 21:00:00

○ Task #2: Call dentist
  Created: 2026-01-04 21:05:00

○ Task #3: Write report
  Description: Q4 performance analysis
  Created: 2026-01-04 21:10:00
```

**Visual Indicators:**
- `✓` = Completed task
- `○` = Incomplete task

## Feature 3: Delete Task

Remove tasks you no longer need.

### Command
```
todo> delete <task_id>
```

### Examples
```
todo> delete 1
✓ Task #1 deleted: Buy groceries

todo> delete 999
✗ Error: Task #999 not found
```

### Notes
- Deletion is permanent (cannot be undone)
- Requires valid task ID
- Other tasks remain unaffected

## Feature 4: Update Task

Modify title or description of existing tasks.

### Command
```
todo> update <task_id> <field> <value>
```

### Fields
- `title` - Update the task title
- `description` - Update the task description

### Examples

**Update Title:**
```
todo> update 1 title Buy organic groceries
✓ Task #1 updated

todo> update 2 title Call dentist for annual checkup
✓ Task #2 updated
```

**Update Description:**
```
todo> update 3 description Q4 2025 performance report
✓ Task #3 updated
```

**Update with Multi-Word Values:**
```
todo> update 1 title This is a long task name
✓ Task #1 updated
```

### Error Handling
```
todo> update 1 title
✗ Error: Missing required arguments

todo> update 999 title New title
✗ Error: Task #999 not found

todo> update 1 title
✗ Error: Task title cannot be empty
```

## Feature 5: Mark as Complete

Toggle task completion status on/off.

### Command
```
todo> complete <task_id>
```

### Examples

**Mark as Complete:**
```
todo> complete 1
✓ Task #1 marked as complete
```

**Mark as Incomplete (toggle back):**
```
todo> complete 1
✓ Task #1 marked as incomplete
```

**Multiple Toggles:**
```
todo> complete 1    # Now complete
✓ Task #1 marked as complete

todo> complete 1    # Now incomplete
✓ Task #1 marked as incomplete

todo> complete 1    # Now complete again
✓ Task #1 marked as complete
```

### Viewing Completed Tasks
```
todo> list

--- All Tasks (2) ---

✓ Task #1: Buy groceries
  Created: 2026-01-04 21:00:00

○ Task #2: Call dentist
  Created: 2026-01-04 21:05:00
```

## Complete Workflow Example

Here's a typical workflow using all 5 features:

```bash
# Start the app
python3 main.py

# 1. Add some tasks
todo> add Buy groceries
✓ Task #1 added: Buy groceries

todo> add Team meeting | Discuss Q1 goals
✓ Task #2 added: Team meeting

todo> add Send emails
✓ Task #3 added: Send emails

# 2. View all tasks
todo> list
--- All Tasks (3) ---
○ Task #1: Buy groceries
○ Task #2: Team meeting
○ Task #3: Send emails

# 3. Complete a task
todo> complete 1
✓ Task #1 marked as complete

# 4. Update a task
todo> update 2 description Discuss Q1 goals and new features
✓ Task #2 updated

# 5. Delete a task
todo> delete 3
✓ Task #3 deleted: Send emails

# 6. View final state
todo> list
--- All Tasks (2) ---
✓ Task #1: Buy groceries
○ Task #2: Team meeting
  Description: Discuss Q1 goals and new features

# Exit
todo> exit
Goodbye!
```

## All Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <title>` | Add task (simple) | `add Buy milk` |
| `add <title> \| <desc>` | Add with description | `add Meeting \| Q1 review` |
| `list` | View all tasks | `list` |
| `delete <id>` | Delete a task | `delete 1` |
| `update <id> <field> <val>` | Update task | `update 1 title New name` |
| `complete <id>` | Toggle completion | `complete 1` |
| `help` | Show help | `help` |
| `exit` | Quit app | `exit` |

## Testing

### Run All Tests
```bash
python3 test_all_features.py
```

### Run Feature Demo
```bash
python3 demo_all_features.py
```

## Tips

1. **No quotes needed for add**: For simple tasks, just type naturally
2. **Use pipe for descriptions**: Separate title and description with `|`
3. **Task IDs**: Use `list` to see task IDs before updating/deleting
4. **Multi-word values**: The app handles spaces automatically
5. **Press Ctrl+C**: If you get stuck, press Ctrl+C then type `exit`

## Important Notes

⚠️ **In-Memory Only**: All tasks are stored in memory and will be **lost when you exit** the application. This is by design (no database or file persistence).

✅ **All 5 Features**: Add, View, Delete, Update, Mark Complete
✅ **24 Tests**: All tests passing
✅ **Spec-Driven**: Every feature has a specification
