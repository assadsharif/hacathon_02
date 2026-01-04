# Feature Specification: Update Task

## Feature Name
**Update Task**

## User Story
As a user, I want to update a task's details so I can modify the title or description of existing tasks.

## Acceptance Criteria

### AC1: Task ID Required
- User must provide a task ID to update
- ID must be an integer
- Task with the specified ID must exist

### AC2: Title Update (Optional)
- User can update the task title
- New title must be non-empty if provided
- If not provided, title remains unchanged

### AC3: Description Update (Optional)
- User can update the task description
- Description can be set to None (remove description)
- If not provided, description remains unchanged

### AC4: At Least One Field Required
- At least one field (title or description) must be provided for update
- If neither provided, display error

### AC5: Task Updated in Storage
- The task is updated in in-memory storage
- Task ID and created_at remain unchanged
- Only specified fields are modified

### AC6: Confirmation Message
- Upon successful update, display confirmation message
- Message should include task ID
- Format: `"✓ Task #{id} updated"`

### AC7: Error Handling
- If task ID does not exist, display error: `"✗ Error: Task #{id} not found"`
- If no fields provided, display error: `"✗ Error: No fields to update"`
- If new title is empty, display error: `"✗ Error: Task title cannot be empty"`

## Technical Specification

### Function Signature
```python
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict[str, Any]:
    """
    Update an existing task's details.

    Args:
        task_id: The unique task identifier
        title: New task title (optional, must be non-empty if provided)
        description: New task description (optional, can be None to remove)

    Returns:
        Dictionary containing updated task details:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If task not found, no fields provided, or title is empty
    """
    pass
```

## Testing Scenarios

### Test Case 1: Update Title Only
```python
# Setup
add_task("Buy groceries")  # ID: 1

# Input
update_task(task_id=1, title="Buy organic groceries")

# Expected Output
{
    'id': 1,
    'title': "Buy organic groceries",
    'description': None,
    'completed': False,
    'created_at': <original_datetime>
}

# Expected Console Output
"✓ Task #1 updated"
```

### Test Case 2: Update Description Only
```python
# Setup
add_task("Write report", "Q4 performance")  # ID: 1

# Input
update_task(task_id=1, description="Q1 performance for 2026")

# Expected Output
{
    'id': 1,
    'title': "Write report",
    'description': "Q1 performance for 2026",
    'completed': False,
    'created_at': <original_datetime>
}
```

### Test Case 3: Update Both Title and Description
```python
# Setup
add_task("Meeting")  # ID: 1

# Input
update_task(task_id=1, title="Team Meeting", description="Discuss new project")

# Expected Output
{
    'id': 1,
    'title': "Team Meeting",
    'description': "Discuss new project",
    'completed': False,
    'created_at': <original_datetime>
}
```

### Test Case 4: Update Non-Existent Task
```python
# Input
update_task(task_id=999, title="New title")

# Expected Behavior
- Raise ValueError
- Console Output: "✗ Error: Task #999 not found"
```

### Test Case 5: Update with Empty Title
```python
# Setup
add_task("Buy groceries")  # ID: 1

# Input
update_task(task_id=1, title="")

# Expected Behavior
- Raise ValueError
- Console Output: "✗ Error: Task title cannot be empty"
```

## Success Criteria
- ✅ Function signature matches specification
- ✅ All acceptance criteria met
- ✅ All test cases pass
- ✅ Partial updates work correctly
- ✅ ID and created_at remain unchanged
- ✅ Error handling works correctly
