# Feature Specification: Add Task

## Feature Name
**Add Task**

## User Story
As a user, I want to add a new task to my list so I can remember it.

## Acceptance Criteria

### AC1: Title Input (Required)
- User can input a task title
- Title must be a string
- Title is **required** (cannot be empty or None)
- If title is empty, system should reject the task creation

### AC2: Description Input (Optional)
- User can input an optional description
- Description must be a string
- Description defaults to `None` if not provided
- Empty string descriptions are allowed

### AC3: Unique ID Assignment
- The system assigns a unique ID to each task
- ID should be an integer
- IDs should increment sequentially (1, 2, 3, ...)
- IDs must be unique across all tasks

### AC4: In-Memory Storage
- The task is stored in memory (not persisted to disk or database)
- Task data structure must include:
  - `id`: int (unique identifier)
  - `title`: str (task title)
  - `description`: str | None (optional description)
  - `completed`: bool (default: False)
  - `created_at`: datetime (timestamp of creation)

### AC5: Confirmation Message
- Upon successful task creation, display a confirmation message
- Message should include:
  - Task ID
  - Task title
- Format: `"✓ Task #{id} added: {title}"`

### AC6: Error Handling
- If title is empty or None, display error: `"✗ Error: Task title is required"`
- No task should be created if validation fails

## Technical Specification

### Function Signature
```python
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
    pass
```

### Data Structure: Task
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
```

### In-Memory Storage
```python
# Global in-memory task storage
tasks: list[Task] = []

# Task ID counter
_task_id_counter: int = 0
```

## Implementation Notes

### Constraints
- All operations must use in-memory data structures
- No file I/O or database operations
- Task IDs start from 1 and increment

### Validation Rules
1. Title must not be None
2. Title must not be an empty string after stripping whitespace
3. Description can be None or any string

### ID Generation Strategy
- Use a module-level counter `_task_id_counter`
- Increment counter before assignment
- Ensures unique, sequential IDs

## Testing Scenarios

### Test Case 1: Valid Task with Title Only
```python
# Input
title = "Buy groceries"
description = None

# Expected Output
{
    'id': 1,
    'title': "Buy groceries",
    'description': None,
    'completed': False,
    'created_at': <datetime>
}

# Expected Console Output
"✓ Task #1 added: Buy groceries"
```

### Test Case 2: Valid Task with Title and Description
```python
# Input
title = "Write report"
description = "Quarterly performance report for Q4"

# Expected Output
{
    'id': 2,
    'title': "Write report",
    'description': "Quarterly performance report for Q4",
    'completed': False,
    'created_at': <datetime>
}

# Expected Console Output
"✓ Task #2 added: Write report"
```

### Test Case 3: Invalid Task - Empty Title
```python
# Input
title = ""
description = "Some description"

# Expected Behavior
- Raise ValueError
- No task created
- Console Output: "✗ Error: Task title is required"
```

### Test Case 4: Invalid Task - None Title
```python
# Input
title = None
description = "Some description"

# Expected Behavior
- Raise ValueError
- No task created
- Console Output: "✗ Error: Task title is required"
```

## Dependencies
- Python standard library only
- `dataclasses` module
- `datetime` module
- No external dependencies

## Success Criteria
- ✅ Function signature matches specification
- ✅ Task data structure implemented as specified
- ✅ All acceptance criteria met
- ✅ All test cases pass
- ✅ Error handling works correctly
- ✅ Confirmation messages display properly
- ✅ Tasks stored in memory (no persistence)
