# Quickstart Guide: Add Task Feature

**Feature**: 001-add-task
**Date**: 2026-01-10
**Target Audience**: Developers implementing and testing the feature

## Overview

This guide provides quick instructions for implementing, testing, and using the Add Task feature. Follow the TDD (Test-Driven Development) workflow as mandated by the project constitution.

## Prerequisites

- Python 3.13+ installed
- Project cloned and on branch `001-add-task`
- Virtual environment activated
- Dependencies installed: `uv sync --dev`

## Implementation Workflow

### Step 1: Write Tests First (RED)

Following TDD principles, write tests **before** implementing code.

**Create test file**: `tests/unit/test_add_task.py`

```python
from datetime import datetime
import pytest
from src.task_manager import add_task
from src.storage import _tasks, _task_id_counter

def test_add_task_with_title_only():
    """Test adding a task with only a title."""
    task = add_task("Buy groceries")

    assert task['id'] == 1
    assert task['title'] == "Buy groceries"
    assert task['description'] is None
    assert task['completed'] is False
    assert isinstance(task['created_at'], datetime)

def test_add_task_with_description():
    """Test adding a task with title and description."""
    task = add_task("Write report", "Q4 performance report")

    assert task['title'] == "Write report"
    assert task['description'] == "Q4 performance report"

def test_add_task_empty_title_raises_error():
    """Test that empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title is required"):
        add_task("")

def test_add_task_none_title_raises_error():
    """Test that None title raises ValueError."""
    with pytest.raises(ValueError, match="Task title is required"):
        add_task(None)

def test_add_task_whitespace_title_raises_error():
    """Test that whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Task title is required"):
        add_task("   ")

def test_task_ids_are_sequential():
    """Test that task IDs increment sequentially."""
    task1 = add_task("Task 1")
    task2 = add_task("Task 2")
    task3 = add_task("Task 3")

    assert task1['id'] == 1
    assert task2['id'] == 2
    assert task3['id'] == 3
```

**Run tests** (they should FAIL):
```bash
pytest tests/unit/test_add_task.py -v
```

Expected output: All tests fail because functions don't exist yet.

### Step 2: Implement Code (GREEN)

Now implement the minimum code to make tests pass.

**File: `src/models.py`**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """Represents a task in the todo list."""
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
```

**File: `src/storage.py`**
```python
from src.models import Task

# In-memory storage
_tasks: list[Task] = []

# ID counter
_task_id_counter: int = 0

def _generate_task_id() -> int:
    """Generate next sequential task ID."""
    global _task_id_counter
    _task_id_counter += 1
    return _task_id_counter
```

**File: `src/task_manager.py`**
```python
from datetime import datetime
from typing import Any
from src.models import Task
from src.storage import _tasks, _generate_task_id

def add_task(title: str, description: str | None = None) -> dict[str, Any]:
    """
    Add a new task to the in-memory task list.

    Args:
        title: The task title (required, non-empty)
        description: Optional task description

    Returns:
        Dictionary containing task details:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If title is empty or None
    """
    # Validate title
    if title is None or not title.strip():
        print("✗ Error: Task title is required")
        raise ValueError("Task title is required")

    # Generate ID and timestamp
    task_id = _generate_task_id()
    created_at = datetime.now()

    # Create task
    task = Task(
        id=task_id,
        title=title.strip(),
        description=description,
        completed=False,
        created_at=created_at
    )

    # Store task
    _tasks.append(task)

    # Display confirmation
    print(f"✓ Task #{task.id} added: {task.title}")

    # Return task as dictionary
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'completed': task.completed,
        'created_at': task.created_at
    }
```

**Run tests** (they should PASS):
```bash
pytest tests/unit/test_add_task.py -v
```

Expected output: All tests pass.

### Step 3: Refactor (REFACTOR)

Review code for improvements while keeping tests passing.

**Checklist**:
- ✓ PEP 8 compliance
- ✓ Type hints on all functions
- ✓ Docstrings present
- ✓ No code duplication
- ✓ Clear variable names
- ✓ Separation of concerns

**Run tests again** after refactoring:
```bash
pytest tests/unit/test_add_task.py -v
```

All tests should still pass.

## Usage Examples

### Basic Usage

```python
from src.task_manager import add_task

# Add a simple task
task = add_task("Buy groceries")
# Output: ✓ Task #1 added: Buy groceries
# Returns: {'id': 1, 'title': 'Buy groceries', 'description': None, ...}

# Add a task with description
task = add_task("Write report", "Quarterly performance report for Q4")
# Output: ✓ Task #2 added: Write report
# Returns: {'id': 2, 'title': 'Write report', 'description': 'Quarterly...', ...}
```

### Error Handling

```python
from src.task_manager import add_task

# Invalid: Empty title
try:
    add_task("")
except ValueError as e:
    print(f"Caught error: {e}")
    # Output: ✗ Error: Task title is required
    #         Caught error: Task title is required

# Invalid: None title
try:
    add_task(None)
except ValueError as e:
    print(f"Caught error: {e}")
    # Output: ✗ Error: Task title is required

# Invalid: Whitespace only
try:
    add_task("   ")
except ValueError as e:
    print(f"Caught error: {e}")
    # Output: ✗ Error: Task title is required
```

### Accessing Stored Tasks

```python
from src.storage import _tasks

# Add some tasks
add_task("Task 1")
add_task("Task 2")

# Access all tasks
print(f"Total tasks: {len(_tasks)}")  # Output: Total tasks: 2

# Iterate over tasks
for task in _tasks:
    print(f"#{task.id}: {task.title}")
    # Output:
    # #1: Task 1
    # #2: Task 2
```

## Running Tests

### Run All Add Task Tests
```bash
pytest tests/unit/test_add_task.py -v
```

### Run with Coverage
```bash
pytest tests/unit/test_add_task.py --cov=src.task_manager --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### Run Specific Test
```bash
pytest tests/unit/test_add_task.py::test_add_task_with_title_only -v
```

## Common Issues & Troubleshooting

### Issue: Tests fail with "ModuleNotFoundError"

**Cause**: Python path not set or virtual environment not activated

**Solution**:
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: ID counter doesn't reset between tests

**Cause**: Global state persists across tests

**Solution**: Add fixture to reset state
```python
import pytest

@pytest.fixture(autouse=True)
def reset_storage():
    """Reset task storage before each test."""
    from src.storage import _tasks, _task_id_counter
    _tasks.clear()
    # Reset counter (requires adding reset function in storage.py)
```

### Issue: Timestamp comparison fails in tests

**Cause**: Datetime comparison precision issues

**Solution**: Check type instead of exact value
```python
from datetime import datetime

task = add_task("Test")
assert isinstance(task['created_at'], datetime)  # Type check
# Don't: assert task['created_at'] == datetime.now()  # Timing issue
```

## Next Steps

After completing this feature:

1. ✅ All tests pass
2. ✅ Code follows PEP 8
3. ✅ Coverage > 90%
4. → Run `/sp.tasks` to generate implementation tasks
5. → Proceed to next feature (delete-task, mark-complete, etc.)

## Integration with Other Features

This feature provides the foundation for:
- **List Tasks**: Display all created tasks
- **Update Task**: Modify task title/description
- **Delete Task**: Remove tasks from list
- **Mark Complete**: Toggle task completion status

All future features will depend on the Task model and storage defined here.

## Reference

- **Spec**: `specs/001-add-task/spec.md`
- **Plan**: `specs/001-add-task/plan.md`
- **Data Model**: `specs/001-add-task/data-model.md`
- **Research**: `specs/001-add-task/research.md`

