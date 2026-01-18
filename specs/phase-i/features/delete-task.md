# Feature Specification: Delete Task

## Feature Name
**Delete Task**

## User Story
As a user, I want to delete a task from my list so I can remove tasks I no longer need.

## Acceptance Criteria

### AC1: Task ID Required
- User must provide a task ID to delete
- ID must be an integer
- If ID is not provided, system should reject the operation

### AC2: Task Exists
- The task with the specified ID must exist in the list
- If task does not exist, display error message
- No other tasks should be affected

### AC3: Task Removal
- The task is removed from in-memory storage
- Task is permanently deleted (cannot be recovered)
- Task count decreases by 1

### AC4: Confirmation Message
- Upon successful deletion, display confirmation message
- Message should include the deleted task ID and title
- Format: `"✓ Task #{id} deleted: {title}"`

### AC5: Error Handling
- If task ID does not exist, display error: `"✗ Error: Task #{id} not found"`
- If ID is invalid (not a number), display error: `"✗ Error: Invalid task ID"`

## Technical Specification

### Function Signature
```python
def delete_task(task_id: int) -> dict[str, Any] | None:
    """
    Delete a task from the in-memory task list.

    Args:
        task_id: The unique task identifier

    Returns:
        Dictionary containing deleted task details if found, None otherwise:
        {
            'id': int,
            'title': str,
            'description': str | None,
            'completed': bool,
            'created_at': datetime
        }

    Raises:
        ValueError: If task with specified ID does not exist
    """
    pass
```

## Testing Scenarios

### Test Case 1: Delete Existing Task
```python
# Setup: Add tasks
add_task("Buy groceries")  # ID: 1
add_task("Call dentist")   # ID: 2

# Input
task_id = 1

# Expected Output
{
    'id': 1,
    'title': "Buy groceries",
    'description': None,
    'completed': False,
    'created_at': <datetime>
}

# Expected Console Output
"✓ Task #1 deleted: Buy groceries"

# Verification
get_all_tasks() should return only 1 task (ID: 2)
```

### Test Case 2: Delete Non-Existent Task
```python
# Input
task_id = 999

# Expected Behavior
- Raise ValueError
- Console Output: "✗ Error: Task #999 not found"
- No tasks deleted
```

## Success Criteria
- ✅ Function signature matches specification
- ✅ All acceptance criteria met
- ✅ All test cases pass
- ✅ Error handling works correctly
- ✅ Task count updates correctly
- ✅ Other tasks remain unaffected
