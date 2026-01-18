# Feature Specification: Sort Tasks

## Feature Name
**Sort Tasks**

## User Story
As a user, I want to sort my tasks by different criteria so I can view them in my preferred order.

## Acceptance Criteria

### AC1: Sort by ID
- Tasks sorted by ID (ascending or descending)
- Default sort order

### AC2: Sort by Title
- Tasks sorted alphabetically by title
- Case-insensitive sorting

### AC3: Sort by Created Date
- Tasks sorted by creation timestamp
- Newest first or oldest first

### AC4: Sort by Completion Status
- Completed tasks grouped separately from incomplete
- Within each group, maintain ID order

## Technical Specification

### Function Signature
```python
def get_sorted_tasks(sort_by: str = "id", reverse: bool = False) -> list[Task]:
    """
    Get tasks sorted by specified criteria.

    Args:
        sort_by: Sort criterion ("id", "title", "created", "status")
        reverse: Sort in reverse order (default: False)

    Returns:
        List of Task objects sorted by the specified criterion
    """
    pass
```

## Testing Scenarios

### Test Case 1: Sort by ID (default)
```python
# Setup
add_task("Task C")  # ID: 1
add_task("Task A")  # ID: 2
add_task("Task B")  # ID: 3

# Input
sort_by = "id"

# Expected
Returns tasks in order: 1, 2, 3
```

### Test Case 2: Sort by Title
```python
# Input
sort_by = "title"

# Expected
Returns tasks in order: "Task A", "Task B", "Task C"
```

### Test Case 3: Sort by Status
```python
# Setup
add_task("Task 1")
add_task("Task 2")
add_task("Task 3")
toggle_task_completion(2)

# Input
sort_by = "status"

# Expected
Incomplete tasks first, then completed tasks
```

## Success Criteria
- ✅ All sort criteria work correctly
- ✅ Reverse sorting works
- ✅ Case-insensitive title sorting
- ✅ Default sort is by ID
